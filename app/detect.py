import os
import json
import logging
import datetime as dt

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for, make_response, send_from_directory)
from werkzeug.exceptions import abort

from app.db import get_db, close_db

# belong to detect.py
import cv2
from PIL import Image
import numpy as np
from packages.yolov3 import main as yolov3
from packages.opencv import main as opencv

bp = Blueprint('detect', __name__)


@bp.route('/upload', methods=['POST'])
def upload():

    root = os.getcwd()
    result = {}

    file = request.files['file']
    filename = file.filename.split(".")[0]

    img_raw = Image.open(file).convert("RGB")

    os.chdir("./packages/yolov3/")

    logging.info("begin detect...")
    image, cropped = yolov3.detect(img_raw)
    logging.info(cropped)
    result = json.dumps(cropped, ensure_ascii=False).encode('utf-8')

    os.chdir(root)

    # clock images collection
    try:
        count = 0
        for i in cropped['clock']:
            img_crop = img_raw.crop(
                (i[0] - 20, i[1] - 20, i[2] + 20, i[3] + 20))
            img_crop.save("./out/clock_" + str(count) + ".jpg")

            img_input = cv2.cvtColor(np.asarray(img_crop), cv2.COLOR_RGB2BGR)

            x, y, r = opencv.calibrate(img_input)
            img_output = opencv.draw_calibration(img_input)
            cv2.imwrite("./out/clock_" + str(count) + "_calibrate.jpg",
                        img_output)

            count += 1
    except Exception as err:
        logging.exception(err)

    # tvmonitor images collection
    try:
        count = 0
        for i in cropped['tvmonitor']:
            img_crop = img_raw.crop(
                (i[0] - 20, i[1] - 20, i[2] + 20, i[3] + 20))
            img_crop.save("./out/tvmonitor_" + str(count) + ".jpg")
            image.save("./out/tvmonitor_" + str(count) + "_marked.jpg")
            count += 1
    except Exception as err:
        logging.exception(err)

    return result, 200, {"ContentType": "application/json"}
