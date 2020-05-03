import os
import json
import logging
import functools
import requests

import pandas as pd
from pyecharts.charts import Line

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for, make_response, send_from_directory)
from werkzeug.exceptions import abort

from app.config import webcam_op
from app.db import get_db, close_db
from app import utils
from app import detect

bp = Blueprint('server', __name__)


def line_smooth(date, value) -> Line:
    c = (Line().add_xaxis(date).add_yaxis("Value", value, is_smooth=True))
    return c


@bp.route('/data', methods=['POST'])
def data():
    device_id = request.form['id']
    db = get_db()
    sql = 'SELECT * FROM `records` WHERE `device_id`={device_id} ORDER BY id'.format(
        device_id=device_id)
    result = db.fetchall(sql)

    date = []
    value = []
    for _, row in result.iterrows():
        date.append("{:%Y-%m-%d %H:%M:%S}".format(row['time'].to_pydatetime()))
        value.append(row['value'])
    close_db()

    c = line_smooth(date[-10:], value[-10:])
    return c.dump_options_with_quotes()


@bp.route('/preview', methods=['POST'])
def preview():
    from io import BytesIO

    try:
        deviceAddress = request.form["deviceAddress"]
        response = requests.get(deviceAddress + webcam_op['photo'])
        img = BytesIO(response.content)
        # with open('./images/0.png', 'rb') as f:
        #     a = f.read()
        #     img = BytesIO(a)
        dial_gauge_num = detect.preview(img)

    except Exception as e:
        logging.debug(e)
        abort(500)

    return {"dial_gauge_num": dial_gauge_num}


@bp.route('/getPreview', methods=['get'])
def getPreview():
    with open(os.path.join("out", "preview.png"), "rb") as f:
        img = f.read()
        response = make_response(img)
        response.headers['Content-Type'] = 'image/png'
        return response


@bp.route('/calibrate', methods=['POST'])
def calibrate():
    from io import BytesIO

    try:
        deviceAddress = request.form["deviceAddress"]
        deviceNum = int(request.form["deviceNum"])
        response = requests.get(deviceAddress + webcam_op['photo'])
        img = BytesIO(response.content)
        # with open('./images/0.png', 'rb') as f:
        #     a = f.read()
        #     img = BytesIO(a)
        x, y, r = detect.calibrate(img, deviceNum)
    except Exception as e:
        logging.debug(e)
        abort(500)

    return {'x': x, 'y': y, 'r': r}


@bp.route('/getCalibrate', methods=['get'])
def getCalibrate():
    with open(os.path.join("out", "dial_gauge_calibrate.jpg"), "rb") as f:
        img = f.read()
        response = make_response(img)
        response.headers['Content-Type'] = 'image/png'
        return response


@bp.route('/config/testDatabase', methods=['POST'])
def testDatabase():
    username = request.form['username']
    password = request.form['password']
    if utils.testDatabase(username, password):
        return 'Ok'
    else:
        return 'error'


@bp.route('/config/saveDatabase', methods=['POST'])
def saveDatabase():
    username = request.form['username']
    password = request.form['password']
    if utils.testDatabase(username, password):
        with open(os.path.join('instance', 'mysql.conf.json'), 'w') as f:
            json.dump({
                'MYSQL_USERNAME': username,
                'MYSQL_PASSWORD': password
            },
                      f,
                      ensure_ascii=False)
        return 'Ok'
    else:
        return 'error'


@bp.route('/config/initDatabase', methods=['POST'])
def initDatabase():
    try:
        db = get_db()
        db.create()
        close_db()
        return 'Ok'
    except Exception as err:
        if err.args[0] != 1065:
            return str(err)
        else:
            return 'Ok'


@bp.route('/config/resetDatabase', methods=['POST'])
def resetDatabase():
    try:
        db = get_db()
        db.clear()
        db.create()
        close_db()
        return 'Ok'
    except Exception as err:
        if err.args[0] != 1065:
            return str(err)
        else:
            return 'Ok'


@bp.route('/config/saveDevice', methods=['POST'])
def saveDevice():
    name = request.form['deviceName']
    address = request.form['deviceAddress']
    type = request.form['deviceType']
    num = request.form['deviceNum']
    minAngle = request.form["minAngle"]
    maxAngle = request.form["maxAngle"]
    minValue = request.form["minValue"]
    maxValue = request.form["maxValue"]
    x = request.form["x"]
    y = request.form["y"]
    r = request.form["r"]
    try:
        unit = "'" + request.form["unit"] + "'"
    except:
        unit = "NULL"
    try:
        description = "'" + request.form["description"] + "'"
    except:
        description = "NULL"

    sql = "INSERT INTO `device_info` (`name`, `address`, `type`, `num`, `minAngle`, `maxAngle`, `minValue`, `maxValue`, `unit`, `description`, `x`, `y`, `r`) VALUES ('{name}', '{address}', '{type}', '{num}', {minAngle}, {maxAngle}, {minValue}, {maxValue}, {unit}, {description}, {x}, {y}, {r})".format(
        name=name,
        address=address,
        type=type,
        num=num,
        minAngle=minAngle,
        maxAngle=maxAngle,
        minValue=minValue,
        maxValue=maxValue,
        unit=unit,
        description=description,
        x=x,
        y=y,
        r=r)
    db = get_db()
    db.execute(sql)
    db.commit()
    close_db()

    os.system("sh ocr.sh")

    return 'Ok'


@bp.route('/config/deleteDevice', methods=['POST'])
def deleteDevice():
    device_id = request.form['device_id']
    sql = "DELETE FROM `device_info` WHERE `id`={device_id}".format(
        device_id=device_id)
    db = get_db()
    db.execute(sql)
    db.commit()
    close_db()

    os.system("sh ocr.sh")

    return 'Ok'