from flask import Blueprint, session, redirect, url_for

home = Blueprint('home', __name__)

from .views import user, code

"""
这里是对所有的加访问控制，登录不需要加，所以在这里不合适
@home.before_request
def process_request():
    if not session.get('user_info'):
        return redirect(url_for('home.user_login'))
"""
