import os
import json
import logging
import functools
import requests

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for, make_response, send_from_directory)
from werkzeug.exceptions import abort

from app.config import webcam_op
from app.db import get_db, close_db
from app import utils
from app import detect

bp = Blueprint('server', __name__)


@bp.route('/data', methods=['GET'])
def data():
    return {'result': 'Ok'}


@bp.route('/calibrate', methods=['POST'])
def calibrate():
    from io import BytesIO

    try:
        deviceName = request.form["deviceName"]
        deviceAddress = request.form["deviceAddress"]
        response = requests.get(deviceAddress + webcam_op['photo'])
        img = BytesIO(response.content)
        detect.calibrate(img)

        return "Ok"
    except Exception as e:
        logging.debug(e)
        abort(500)


@bp.route('/getCalibrate', methods=['get'])
def getCalibrate():
    with open(os.path.join("out", "clock_0_calibrate.jpg"), "rb") as f:
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
    minAngle = request.form["minAngle"]
    maxAngle = request.form["maxAngle"]
    minValue = request.form["minValue"]
    maxValue = request.form["maxValue"]
    try:
        unit = "'" + request.form["unit"] + "'"
    except:
        unit = "NULL"
    try:
        description = "'" + request.form["description"] + "'"
    except:
        description = "NULL"

    sql = "INSERT INTO `device_info` (`name`, `address`, `minAngle`, `maxAngle`, `minValue`, `maxValue`, `unit`, `description`) VALUES ('{name}', '{address}', {minAngle}, {maxAngle}, {minValue}, {maxValue}, {unit}, {description})".format(
        name=name,
        address=address,
        minAngle=minAngle,
        maxAngle=maxAngle,
        minValue=minValue,
        maxValue=maxValue,
        unit=unit,
        description=description)
    db = get_db()
    db.execute(sql)
    db.commit()
    close_db()

    return 'Ok'