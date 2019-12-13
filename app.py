import os
import json
import logging
import datetime as dt
from flask import Flask, request, redirect, url_for

from PIL import Image
from packages.yolov3 import app as yolov3

root = os.getcwd()
app = Flask(__name__)


@app.route('/', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename.split(".")[0]

    image = Image.open(file).convert("RGB")
    os.chdir("./packages/yolov3/")
    image, cropped = yolov3.detect(image)
    os.chdir(root)
    image.savefig("./out/temp.png", bbox_inches="tight", pad_inches=0.0)
    logging.info(cropped)

    result = json.dumps(cropped, ensure_ascii=False).encode('utf-8')

    return result, 200, {"ContentType": "application/json"}


if __name__ == '__main__':
    os.makedirs("./out/", exist_ok=True)
    os.makedirs("./log/", exist_ok=True)
    logging.basicConfig(filename="./log/app.log",
                        filemode="a",
                        format="%(asctime)s %(levelname)s:%(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        level=logging.DEBUG)

    app.run(host='localhost', port=8000, debug=True)