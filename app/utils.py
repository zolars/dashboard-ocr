import os
import logging
import functools

from flask import (Blueprint, flash, g, redirect, render_template, url_for)
from werkzeug.exceptions import abort

from app.db import get_db, close_db


def config_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        try:
            db = get_db()
            close_db()
        except Exception as e:
            logging.error(e)
            flash('Welcome! Please Initialize Your Configurations', 'notice')
            return redirect(url_for('pages.database'))

        return view(**kwargs)

    return wrapped_view
