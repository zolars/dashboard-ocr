import os
import json
import logging
import requests
import pymysql
import pandas as pd
from io import BytesIO
import threading
import multiprocessing

import cv2
from PIL import Image
import numpy as np
from packages.yolov3 import main as yolov3
from packages.opencv import main as opencv

from app.config import webcam_op


class MySQL:
    def __init__(self, username, password):
        try:
            self._conn = pymysql.connect(
                host='localhost',  # mysql server address
                port=3306,  # port num
                user=username,  # username
                passwd=password,  # password
                db='dashboard',
                charset='utf8',
            )
        except:
            self._conn = pymysql.connect(
                host='localhost',  # mysql server address
                port=3306,  # port num
                user=username,  # username
                passwd=password,  # password
                charset='utf8',
            )
        self._cur = self._conn.cursor()

    def execute(self, sql):
        print(sql)
        self._cur.execute(sql)

    def fetchall(self, sql):
        print(sql)
        df = pd.read_sql(sql, con=self._conn)
        return df

    def commit(self):
        self._conn.commit()

    def __del__(self):
        self._conn.close()


def runYOLO(img):
    root = os.getcwd()
    print(root)
    os.chdir("./packages/yolov3/")

    _, cropped = yolov3.detect(img)
    print(cropped)

    os.chdir(root)

    return _, cropped


def calibrate(img):
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

            x, y, r = opencv.calibrate(img_input)
            img_output = opencv.draw_calibration(img_input, x, y, r)
            cv2.imwrite("./out/clock_" + str(count) + "_calibrate.jpg",
                        img_output)

            count += 1

            return x, y, r

    # # tvmonitor images collection
    # if 'tvmonitor' in cropped:
    #     count = 0
    #     for i in cropped['tvmonitor']:
    #         img_crop = img.crop(
    #             (i[0] - 20, i[1] - 20, i[2] + 20, i[3] + 20))
    #         img_crop.save("./out/tvmonitor_" + str(count) + ".jpg")
    #         _.save("./out/tvmonitor_" + str(count) + "_marked.jpg")
    #         count += 1


def ocr(img, min_angle, max_angle, min_value, max_value, x, y, r):
    img = Image.open(img).convert("RGB")
    print("    Run YOLO...")
    _, cropped = runYOLO(img)

    print("    Run OpenCV...")
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


def run(item):

    print("    Requests Get...")
    response = requests.get(item['address'] + webcam_op['photo'])
    img = BytesIO(response.content)
    result = ocr(img, item['minAngle'], item['maxAngle'], item['minValue'],
                 item['maxValue'], item['x'], item['y'], item['r'])
    return result


if __name__ == '__main__':

    print("OCR Server is beginning...")

    with open(os.path.join('instance', 'mysql.conf.json')) as f:
        config = json.load(f)
    username = config['MYSQL_USERNAME']
    password = config['MYSQL_PASSWORD']

    sql = 'SELECT * FROM `device_info` ORDER BY id'
    db = MySQL(username, password)
    results = db.fetchall(sql)

    items = []
    for _, row in results.iterrows():
        items.append({
            'id': row['id'],
            'address': row['address'],
            'minAngle': row['minAngle'],
            'maxAngle': row['maxAngle'],
            'minValue': row['minValue'],
            'maxValue': row['maxValue'],
            'x': row['x'],
            'y': row['y'],
            'r': row['r']
        })

    while (True):
        for item in items:
            print("OCR Start - Device ID : " + str(item["id"]))
            result = run(item)
            sql = "INSERT INTO `records` (`device_id`, `value`) VALUES ({device_id}, {value})".format(
                device_id=item["id"], value=result)
            db.execute(sql)
            db.commit()
            print("OCR Finished - Device ID : " + str(item["id"]) +
                  " Result : " + str(result))
