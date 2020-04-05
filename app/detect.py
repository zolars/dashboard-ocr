import os
import logging
import requests
import datetime as dt
from io import BytesIO
from multiprocessing import Process, Pool

import cv2
from PIL import Image
import numpy as np
from packages.yolov3 import main as yolov3
from packages.opencv import main as opencv

from app.config import webcam_op
from app.db import get_db, close_db


def runYOLO(img):
    root = os.getcwd()

    os.chdir("./packages/yolov3/")

    _, cropped = yolov3.detect(img)
    logging.info(cropped)

    os.chdir(root)

    return _, cropped


def calibrate(img):
    img = Image.open(img).convert("RGB")
    _, cropped = runYOLO(img)

    img_output = None
    # clock images collection
    if 'clock' in cropped:
        count = 0
        results = []
        for i in cropped['clock']:
            img_crop = img.crop((i[0] - 20, i[1] - 20, i[2] + 20, i[3] + 20))
            # img_crop.save("./out/clock_" + str(count) + ".jpg")

            img_input = cv2.cvtColor(np.asarray(img_crop), cv2.COLOR_RGB2BGR)

            x, y, r = opencv.calibrate(img_input)
            img_output = opencv.draw_calibration(img_input, x, y, r)
            cv2.imwrite("./out/clock_" + str(count) + "_calibrate.jpg",
                        img_output)

            results.append({'x': x, 'y': y, 'r': r})
            count += 1

    return results


def ocr(img, min_angle, max_angle, min_value, max_value, x, y, r):
    img = Image.open(img).convert("RGB")
    _, cropped = runYOLO(img)

    img_output = None
    # clock images collection
    if 'clock' in cropped:
        count = 0
        for i in cropped['clock']:
            img_crop = img.crop((i[0] - 20, i[1] - 20, i[2] + 20, i[3] + 20))
            # img_crop.save("./out/clock_" + str(count) + ".jpg")

            img_input = cv2.cvtColor(np.asarray(img_crop), cv2.COLOR_RGB2BGR)
            value = opencv.get_current_value(img_input, min_angle, max_angle,
                                             min_value, max_value, x, y, r)
    return value