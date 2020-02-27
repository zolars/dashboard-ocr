import os
import logging
import datetime as dt

import cv2
from PIL import Image
import numpy as np
from packages.yolov3 import main as yolov3
from packages.opencv import main as opencv


def calibrate(img):

    root = os.getcwd()

    img_raw = Image.open(img).convert("RGB")

    os.chdir("./packages/yolov3/")

    image, cropped = yolov3.detect(img_raw)
    logging.info(cropped)

    os.chdir(root)

    img_output = None
    # clock images collection
    if 'clock' in cropped:
        count = 0
        for i in cropped['clock']:
            img_crop = img_raw.crop(
                (i[0] - 20, i[1] - 20, i[2] + 20, i[3] + 20))
            # img_crop.save("./out/clock_" + str(count) + ".jpg")

            img_input = cv2.cvtColor(np.asarray(img_crop), cv2.COLOR_RGB2BGR)

            x, y, r = opencv.calibrate(img_input)
            img_output = opencv.draw_calibration(img_input, x, y, r)
            cv2.imwrite("./out/clock_" + str(count) + "_calibrate.jpg",
                        img_output)

            count += 1

    # # tvmonitor images collection
    # if 'tvmonitor' in cropped:
    #     count = 0
    #     for i in cropped['tvmonitor']:
    #         img_crop = img_raw.crop(
    #             (i[0] - 20, i[1] - 20, i[2] + 20, i[3] + 20))
    #         img_crop.save("./out/tvmonitor_" + str(count) + ".jpg")
    #         image.save("./out/tvmonitor_" + str(count) + "_marked.jpg")
    #         count += 1
