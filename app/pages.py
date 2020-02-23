import os
import json
import logging
import datetime as dt

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for, make_response, send_from_directory)
from werkzeug.exceptions import abort

from app.db import get_db, close_db
from app.utils import config_required

bp = Blueprint('pages', __name__)


@bp.route('/', methods=['GET'])
@config_required
def dashboard():
    flash('dashboard', 'notice')
    params = {}
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


@bp.route('/config/managedevice', methods=['GET'])
@config_required
def managedevice():
    params = {}
    dicts = {'title': 'Manage device', 'params': params}
    return render_template('/config/managedevice.html', **dicts)


@bp.route('/config/adddevice', methods=['GET'])
@config_required
def adddevice():
    params = {}
    dicts = {'title': 'Add device', 'params': params}
    return render_template('/config/adddevice.html', **dicts)
