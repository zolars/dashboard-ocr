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


@bp.route('/config/database', methods=['GET', 'POST'])
def database():
    params = {'title': 'Database'}
    return render_template('/database.html', **params)


@bp.route('/', methods=['GET', 'POST'])
@config_required
def dashboard():
    flash('test', 'error')
    params = {'title': 'Dashboard'}
    return render_template('/dashboard.html', **params)
