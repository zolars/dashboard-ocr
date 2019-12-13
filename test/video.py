import cv2
import time
from datetime import datetime as dt

cap = cv2.VideoCapture(0)

while (True):
    # get a frame
    ret, frame = cap.read()
    # save images
    cv2.imwrite('./image/{:%Y_%m_%d %H_%M_%S}.jpg'.format(dt.now()), frame)
    time.sleep(1)