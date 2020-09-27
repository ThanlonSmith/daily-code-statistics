from flask import session, redirect, url_for, request
from functools import wraps


def login_wrapper(fuc):
    @wraps(fuc)
    def inner(*args, **kwargs):
        if not session.get('user_info'):
            # return redirect('/user/login/?next={}'.format(request.url))
            return redirect(url_for('home.user_login', next=request.url))
        return fuc(*args, **kwargs)

    return inner
