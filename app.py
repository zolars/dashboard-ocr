import os
import json
import logging
import datetime as dt
from flask import Flask, request, redirect, url_for

from PIL import Image
from packages.yolov3 import main as yolov3

root = os.getcwd()
app = Flask(__name__)


@app.route('/', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename.split(".")[0]

    img_raw = Image.open(file).convert("RGB")
    os.chdir("./packages/yolov3/")
    image, cropped = yolov3.detect(img_raw)
    os.chdir(root)

    result = {}
    logging.info(cropped)
    result = json.dumps(cropped, ensure_ascii=False).encode('utf-8')

    # tvmonitor images collection
    try:
        images_tvmonitor = []
        for i in cropped['tvmonitor']:
            images_tvmonitor.append(img_raw.crop((i[0], i[1], i[2], i[3])))
            images_tvmonitor[-1].save("./out/" + str(len(images_tvmonitor)) +
                                      ".png")
    except:
        pass

    # clock images collection
    try:
        images_clock = []
        for i in cropped['clock']:
            images_clock.append(
                img_raw.crop((i[0] - 15, i[1], i[2], i[3] + 15)))
            images_clock[-1].save("./out/" + str(len(images_clock)) + ".png")
    except:
        pass

    return result, 200, {"ContentType": "application/json"}


if __name__ == '__main__':
    os.makedirs("./out/", exist_ok=True)
    os.makedirs("./log/", exist_ok=True)
    logging.basicConfig(filename="./log/app.log",
                        filemode="a",
                        format="%(asctime)s %(levelname)s:%(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        level=logging.ERROR)

    app.run(host='localhost', port=8000, debug=True)