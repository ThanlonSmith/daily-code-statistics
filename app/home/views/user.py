from .. import home
from flask import redirect, render_template, url_for, request, flash, session
from app.utils import md5
from app.utils import db_helper


@home.route('/')
def index():
    return redirect(url_for('home.user_list', page=1))


@home.route('/user/list/<int:page>/')
def user_list(page=None):
    return render_template('home/index.html')


@home.route('/user/login/', methods=['get', 'post'])
def user_login():
    if request.method == 'POST':
        user = request.form.get('user', None)
        pwd = request.form.get('pwd', None)
        print(user, pwd)
        if user and pwd:
            ret = db_helper.fetchone('select *from userinfo where user=%s and pwd=%s', (user, md5.md5(pwd)))
            print(ret)  # {'id': 1, 'user': 'thanlon', 'pwd': 'ea48576f30be1669971699c09ad05c94', 'nickname': 'thanlon'}
            if not ret:
                flash('用户名或者密码错误', 'error')
                return render_template('home/login.html')
            # session['user_id'] = ret['id']
            # session['user_nickname'] = ret['nickname']
            # session['user_info'] = {'user_id': ret['id'], 'user_nickname': ret['nickname']}
            session['user_info'] = ret
            flash('欢迎进入系统！', 'ok')
            return redirect('/')

    return render_template('home/login.html')


@home.route('/user/logout/')
def user_logout():
    print(session, type(session))
    if session.get('user_info'):
        del session['user_info']
    """
    if 'user_info' in session:
        del session['user_info']
    """
    return redirect(url_for('home.user_login', next=request.url))