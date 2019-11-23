import os
import logging
import datetime as dt

from PIL import Image
from packages.yolov3 import app as yolov3

root = os.getcwd()
os.makedirs("./out/", exist_ok=True)
os.makedirs("./log/", exist_ok=True)
logging.basicConfig(filename="./log/test.log",
                    filemode="a",
                    format="%(asctime)s %(levelname)s:%(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.DEBUG)

image = Image.open("./static/1.jpg").convert("RGB")
os.chdir("./packages/yolov3/")
image, cropped = yolov3.detect(image)
os.chdir(root)
image.savefig("./out/temp.png", bbox_inches="tight", pad_inches=0.0)
logging.info(cropped)