import os
import json
import logging
import datetime as dt

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for, make_response, send_from_directory)
from werkzeug.exceptions import abort

from app.db import get_db, close_db
from app.utils import config_required

# dashboard
import requests

bp = Blueprint('pages', __name__)
urls = {
    'pages': {
        'dashboard': '/',
        'database': '/config/database',
    },
    'server': {
        'testDatabase': '/testDatabase',
        'saveDatabase': '/saveDatabase',
        'initDatabase': '/initDatabase',
        'resetDatabase': '/resetDatabase',
    }
}


@bp.route('/', methods=['GET', 'POST'])
@config_required
def dashboard():
    flash('test', 'error')
    params = {}
    dicts = {'title': 'Dashboard', 'params': params, 'urls': urls}
    return render_template('/dashboard.html', **dicts)


@bp.route('/config/database', methods=['GET', 'POST'])
def database():

    params = {}
    if os.path.exists(os.path.join('instance', 'mysql.conf.json')):
        with open(os.path.join('instance', 'mysql.conf.json')) as f:
            config = json.load(f)
            if config['MYSQL_USERNAME'] and config['MYSQL_PASSWORD']:
                params['existedUsername'] = config['MYSQL_USERNAME']
                params['existedPassword'] = config['MYSQL_PASSWORD']

    dicts = {'title': 'Database', 'params': params, 'urls': urls}
    return render_template('/database.html', **dicts)
