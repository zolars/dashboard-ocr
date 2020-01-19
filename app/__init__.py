'''
Run:
export FLASK_APP=app
export FLASK_ENV=development
flask run
'''

import os
import json
import logging
import datetime as dt
from flask import Flask, request, redirect, url_for

import cv2
from PIL import Image
import numpy as np
from ..packages.yolov3 import main as yolov3
from ..packages.opencv import main as opencv


def create_app(test_config=None):

    os.makedirs("./out/", exist_ok=True)
    os.makedirs("./log/", exist_ok=True)
    logging.basicConfig(filename="./log/app.log",
                        filemode="a",
                        format="%(asctime)s %(levelname)s:%(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        level=logging.DEBUG)

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'dashboard-ocrcl.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'hello world!'

    @app.route('/upload', methods=['POST'])
    def upload_file():

        root = os.getcwd()
        result = {}

        file = request.files['file']
        filename = file.filename.split(".")[0]

        img_raw = Image.open(file).convert("RGB")
        os.chdir("./packages/yolov3/")
        # try:
        logging.info("begin detect...")
        image, cropped = yolov3.detect(img_raw)
        logging.info(cropped)
        result = json.dumps(cropped, ensure_ascii=False).encode('utf-8')
        # except Exception as err:
        #     logging.error(err)
        os.chdir(root)

        # clock images collection
        try:
            count = 0
            for i in cropped['clock']:
                img_crop = img_raw.crop(
                    (i[0] - 20, i[1] - 20, i[2] + 20, i[3] + 20))
                img_crop.save("./out/clock_" + str(count) + ".jpg")

                img_input = cv2.cvtColor(np.asarray(img_crop),
                                         cv2.COLOR_RGB2BGR)
                img_output, x, y, r = opencv.calibrate(img_input)
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

    return app