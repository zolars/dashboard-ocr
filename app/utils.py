import os
import json
import logging
import functools

from flask import (Blueprint, flash, g, redirect, render_template, url_for)
from werkzeug.exceptions import abort

from app.db import get_db, close_db


def config_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):

        if os.path.exists(os.path.join('instance', 'mysql.conf.json')):
            with open(os.path.join('instance', 'mysql.conf.json')) as f:
                config = json.load(f)
                if config['MYSQL_USERNAME'] and config['MYSQL_PASSWORD']:
                    if testDatabase(config['MYSQL_USERNAME'],
                                    config['MYSQL_PASSWORD']):
                        return view(**kwargs)
                    else:
                        flash(
                            'There are some problems in your database configurations!',
                            'error')
                        return redirect(url_for('pages.database'))

        flash('Welcome! Please Initialize Your Configurations!', 'notice')
        return redirect(url_for('pages.database'))

    return wrapped_view


def testDatabase(username, password):
    try:
        db = get_db(username=username, password=password)
        close_db()
        return True
    except Exception as e:
        logging.warning(e)
        return False