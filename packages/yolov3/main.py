from __future__ import division

from .models import *
from .utils.utils import *
from .utils.datasets import *

import io
import os
import sys
import time
import logging
import datetime
import argparse

from PIL import Image

import torch
from torch.utils.data import DataLoader
from torchvision import datasets
from torch.autograd import Variable

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.ticker import NullLocator


def detect(img_raw):
    matplotlib.use('agg')
    matplotlib.pyplot.switch_backend('Agg')

    parser = argparse.ArgumentParser()
    parser.add_argument("--model_def",
                        type=str,
                        default="config/yolov3.cfg",
                        help="path to model definition file")
    parser.add_argument("--weights_path",
                        type=str,
                        default="weights/yolov3.weights",
                        help="path to weights file")
    parser.add_argument("--class_path",
                        type=str,
                        default="data/coco.names",
                        help="path to class label file")
    parser.add_argument("--conf_thres",
                        type=float,
                        default=0.8,
                        help="object confidence threshold")
    parser.add_argument("--nms_thres",
                        type=float,
                        default=0.4,
                        help="iou thresshold for non-maximum suppression")
    parser.add_argument("--batch_size",
                        type=int,
                        default=1,
                        help="size of the batches")
    parser.add_argument(
        "--n_cpu",
        type=int,
        default=0,
        help="number of cpu threads to use during batch generation")
    parser.add_argument("--img_size",
                        type=int,
                        default=416,
                        help="size of each image dimension")
    parser.add_argument("--checkpoint_model",
                        type=str,
                        help="path to checkpoint model")
    parser.add_argument("--id",
                        type=int,
                        help="default ocr instruction",
                        default=None)
    parser.add_argument("run",
                        type=str,
                        help="default flask instruction",
                        default=None)
    opt = parser.parse_args()
    logging.info(opt)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Set up model
    model = Darknet(opt.model_def, img_size=opt.img_size).to(device)

    if opt.weights_path.endswith(".weights"):
        # Load darknet weights
        model.load_darknet_weights(opt.weights_path)
    else:
        # Load checkpoint weights
        model.load_state_dict(torch.load(opt.weights_path))

    model.eval()  # Set in evaluation mode

    classes = load_classes(opt.class_path)  # Extracts class labels from file

    Tensor = torch.cuda.FloatTensor if torch.cuda.is_available(
    ) else torch.FloatTensor

    input_img = img_raw
    # Extract image as PyTorch tensor
    input_img = transforms.ToTensor()(input_img)
    # Pad to square resolution
    input_img, _ = pad_to_square(input_img, 0)
    # Resize
    input_img = resize(input_img, opt.img_size)
    # Unsqueeze
    input_img = input_img.unsqueeze(0)

    # Configure input
    input_img = Variable(input_img.type(Tensor))

    logging.info("Performing object detections:")
    prev_time = time.time()

    # Get detections
    with torch.no_grad():
        detections = model(input_img)
        detections = non_max_suppression(detections, opt.conf_thres,
                                         opt.nms_thres)[0]

    # Log progress
    current_time = time.time()
    inference_time = datetime.timedelta(seconds=current_time - prev_time)
    prev_time = current_time
    logging.info("\t+ Inference Time: %s" % (inference_time))

    # Bounding-box colors
    cmap = plt.get_cmap("tab20b")
    colors = [cmap(i) for i in np.linspace(0, 1, 20)]

    # Create plot
    img = np.array(img_raw)
    plt.figure()
    fig, ax = plt.subplots(1)
    ax.imshow(img)
    cropped = {}

    # Draw bounding boxes and labels of detections
    if detections is not None:
        # Rescale boxes to original image
        detections = rescale_boxes(detections, opt.img_size, img.shape[:2])
        unique_labels = detections[:, -1].cpu().unique()
        n_cls_preds = len(unique_labels)
        bbox_colors = random.sample(colors, n_cls_preds)

        count = 0
        for x1, y1, x2, y2, conf, cls_conf, cls_pred in detections:

            logging.info("\t+ Label: %s, Conf: %.5f" %
                         (classes[int(cls_pred)], cls_conf.item()))

            box_w = x2 - x1
            box_h = y2 - y1

            color = bbox_colors[int(
                np.where(unique_labels == int(cls_pred))[0])]
            # Create a Rectangle patch
            bbox = patches.Rectangle((x1, y1),
                                     box_w,
                                     box_h,
                                     linewidth=2,
                                     edgecolor=color,
                                     facecolor="none")
            # Add the bbox to the plot
            ax.add_patch(bbox)
            # Add label
            plt.text(
                x1,
                y1,
                s=classes[int(cls_pred)] + "_" + str(count),
                color="white",
                verticalalignment="top",
                bbox={
                    "color": color,
                    "pad": 0
                },
            )

            # Crop for new images (left, upper, right, lower)
            if classes[int(cls_pred)] not in cropped:
                cropped[classes[int(cls_pred)]] = []
            cropped[classes[int(cls_pred)]].append(
                (x1.item(), y1.item(), x2.item(), y2.item()))

            count += 1

    # Save generated image with detections
    plt.axis("off")
    plt.gca().xaxis.set_major_locator(NullLocator())
    plt.gca().yaxis.set_major_locator(NullLocator())

    # Explicitly closing
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt_bytes = buf.getvalue()
    plt.close()
    buf.close()

    return plt_bytes, cropped
