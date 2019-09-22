# encoding: utf-8

from flask import Flask,redirect,url_for,session
import config
from functools import wraps

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if config.FRONT_USER_ID in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('front.signin'))
    return wrapper