import os
import json
import logging
import click
from flask import current_app, g
from flask.cli import with_appcontext

import pymysql
import pandas as pd
import numpy as np

from app.config import config


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
        self._cur.execute(sql)

    def fetchall(self, sql):
        df = pd.read_sql(sql, con=self._conn)
        return df

    def commit(self):
        self._conn.commit()

    def create(self):
        logging.info("Start to initialize the database...")

        with current_app.open_resource('schema.sql') as f:
            for sql in f.read().decode('utf8').split(';'):
                self._cur.execute(sql)
                self._conn.commit()

    def clear(self):
        logging.info("Start to delete and clear the database...")

        try:
            self._cur.execute('DROP DATABASE IF EXISTS `dashboard`;')
            self._conn.commit()
        except Exception as err:
            logging.error(err)

    def __del__(self):
        self._conn.close()


def get_db(username=None, password=None):
    if not (username or password):
        with open(os.path.join('instance', 'mysql.conf.json')) as f:
            config = json.load(f)
        username = config['MYSQL_USERNAME']
        password = config['MYSQL_PASSWORD']
    if 'db' not in g:
        g.db = MySQL(username, password)
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        del db


def init_app(app):
    app.teardown_appcontext(close_db)
