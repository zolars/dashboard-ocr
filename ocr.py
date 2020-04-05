import os
import json
import logging
import requests
import pymysql
import pandas as pd
from io import BytesIO
import subprocess

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
        logging.info(sql)
        self._cur.execute(sql)

    def fetchall(self, sql):
        logging.info(sql)
        df = pd.read_sql(sql, con=self._conn)
        return df

    def commit(self):
        self._conn.commit()

    def __del__(self):
        self._conn.close()


def runYOLO(img):
    root = os.getcwd()
    os.chdir("./packages/yolov3/")

    _, cropped = yolov3.detect(img)
    logging.info(cropped)

    os.chdir(root)

    return _, cropped


def ocr(img, type, num, min_angle, max_angle, min_value, max_value, x, y, r):
    img = Image.open(img).convert("RGB")
    logging.info("Run YOLO...")
    _, cropped = runYOLO(img)

    logging.info("Run OpenCV...")
    value = None
    # clock images collection
    if 'clock' in cropped:

        i = cropped['clock'][num]
        img_crop = img.crop((i[0] - 20, i[1] - 20, i[2] + 20, i[3] + 20))

        img_input = cv2.cvtColor(np.asarray(img_crop), cv2.COLOR_RGB2BGR)
        value = opencv.get_current_value(img_input, min_angle, max_angle,
                                         min_value, max_value, x, y, r)
    return value


def run(item):

    logging.info("Requests Get...")
    response = requests.get(item['address'] + webcam_op['photo'])
    img = BytesIO(response.content)
    result = ocr(img, item['type'], item['num'], item['minAngle'],
                 item['maxAngle'], item['minValue'], item['maxValue'],
                 item['x'], item['y'], item['r'])
    return result


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='device ID for this script')
    parser.add_argument('--id', type=int, default=None)
    parser.add_argument("run",
                        type=str,
                        help="default flask instruction",
                        default=None)
    args = parser.parse_args()
    device_id = args.id

    if device_id == None:
        logging.basicConfig(filename='./log/ocr.log',
                            filemode="a+",
                            format="%(asctime)s %(levelname)s : %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S",
                            level=logging.DEBUG)

        logging.info("OCR Server is beginning...")

        with open(os.path.join('instance', 'mysql.conf.json')) as f:
            config = json.load(f)
        username = config['MYSQL_USERNAME']
        password = config['MYSQL_PASSWORD']
        db = MySQL(username, password)
        sql = 'SELECT * FROM `device_info` ORDER BY id'.format(
            device_id=device_id)

        df = db.fetchall(sql)

        for _, row in df.iterrows():
            device_id = row['id']
            subprocess.Popen('python ocr.py --id ' + str(device_id) + ' run',
                             executable=None,
                             shell=True)

    else:

        with open(os.path.join('instance', 'mysql.conf.json')) as f:
            config = json.load(f)
        username = config['MYSQL_USERNAME']
        password = config['MYSQL_PASSWORD']
        db = MySQL(username, password)
        sql = 'SELECT * FROM `device_info` WHERE `id`={device_id} ORDER BY id'.format(
            device_id=device_id)

        item = db.fetchall(sql).iloc[0]

        while (True):
            import time

            start = time.time()
            logging.info("OCR Start - Device ID : " + str(item["id"]))
            print("OCR Start - Device ID : " + str(item["id"]))
            result = run(item)
            sql = "INSERT INTO `records` (`device_id`, `value`) VALUES ({device_id}, {value})".format(
                device_id=item["id"], value=result)
            db.execute(sql)
            db.commit()
            logging.info("OCR Finished - Device ID : " + str(item["id"]) +
                         " Result : " + str(result))
            print("OCR Finished - Device ID : " + str(item["id"]) +
                  " Result : " + str(result))
            end = time.time()
            print("%.2fs" % (end - start))
