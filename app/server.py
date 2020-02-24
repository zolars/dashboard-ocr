import os
import json
import logging
import functools
import requests

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for, make_response, send_from_directory)
from werkzeug.exceptions import abort

from app.db import get_db, close_db
from app.utils import config_required
from app import utils

bp = Blueprint('server', __name__)


@bp.route('/getCalibration', methods=['POST'])
def getCalibration():
    try:
        return 'Ok'
    except Exception as e:
        return str(e)


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
    deviceName = request.form['deviceName']
    deviceAddress = request.form['deviceAddress']

    return 'Ok'