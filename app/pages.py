import os
import json
import logging
import datetime as dt

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for, make_response, send_from_directory)
from werkzeug.exceptions import abort

from app.config import webcam_op
from app.db import get_db, close_db
from app.utils import config_required

bp = Blueprint('pages', __name__)


@bp.route('/', methods=['GET'])
@config_required
def dashboard():
    params = {}

    sql = 'SELECT * FROM `device_info` ORDER BY id'
    db = get_db()
    results = db.fetchall(sql)
    close_db()

    items = []
    for _, row in results.iterrows():
        items.append({
            'id': row['id'],
            'name': row['name'],
            'unit': row['unit'],
        })

    params['deviceItems'] = items

    dicts = {'title': 'Dashboard', 'params': params}
    return render_template('/dashboard.html', **dicts)


@bp.route('/config/database', methods=['GET'])
def database():
    params = {}
    if os.path.exists(os.path.join('instance', 'mysql.conf.json')):
        with open(os.path.join('instance', 'mysql.conf.json')) as f:
            config = json.load(f)
            if config['MYSQL_USERNAME'] and config['MYSQL_PASSWORD']:
                params['existedUsername'] = config['MYSQL_USERNAME']
                params['existedPassword'] = config['MYSQL_PASSWORD']

    dicts = {'title': 'Database', 'params': params}
    return render_template('/config/database.html', **dicts)


@bp.route('/config/manageDevice', methods=['GET'])
@config_required
def manageDevice():
    params = {}

    sql = 'SELECT * FROM `device_info` ORDER BY id'
    db = get_db()
    results = db.fetchall(sql)
    close_db()

    items = []
    for _, row in results.iterrows():
        items.append({
            'id': row['id'],
            'name': row['name'],
            'address': row['address'],
            'minAngle': row['minAngle'],
            'maxAngle': row['maxAngle'],
            'minValue': row['minValue'],
            'maxValue': row['maxValue'],
            'unit': row['unit'],
            'description': row['description']
        })

    params['deviceItems'] = items

    dicts = {'title': 'Manage Device', 'params': params}
    return render_template('/config/manageDevice.html', **dicts)


@bp.route('/config/addDevice', methods=['GET'])
@config_required
def addDevice():
    params = {'op': webcam_op}
    dicts = {'title': 'Add Device', 'params': params}
    return render_template('/config/addDevice.html', **dicts)
