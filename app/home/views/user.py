from .decoration import login_wrapper
from .. import home
from flask import redirect, render_template, url_for, request, flash, session
from app.utils import md5
from app.utils import db_helper


@home.route('/')
def index():
    return redirect(url_for('home.user_list', page=1))


@home.route('/user/list/<int:page>/', methods=["GET"])
@login_wrapper
def user_list(page=None):
    if request.method == 'GET':
        per_page = 2  # 每页显示多少条
        # ret = db_helper.fetch_all('select id,user ,nickname from userinfo', ())
        data_list = db_helper.fetch_all('select id,user ,nickname from userinfo limit %s,%s ',
                                        (((page - 1) * per_page), per_page))
        """
         print(data_list)
        [{'id': 1, 'user': 'thanlon', 'nickname': 'thanlon'}, {'id': 2, 'user': 'kiku', 'nickname': 'kiku'}]
        """
        data = db_helper.fetch_all('select id,user ,nickname from userinfo', None)
        sum_count = len(data)  # 总记录数
        if sum_count <= per_page:
            page_num_count = 1
        else:
            if sum_count % per_page == 0:
                page_num_count = sum_count // 1
            else:
                page_num_count = sum_count // 1 + 1

    return render_template('home/index.html', data_list=data_list, page_num_count=page_num_count, page=page)


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


# 退出加装饰器可以不用执行退出逻辑代码，直接退出到登录页面
@home.route('/user/logout/')
@login_wrapper
def user_logout():
    print(session, type(session))
    if session.get('user_info'):
        del session['user_info']
    """
    if 'user_info' in session:
        del session['user_info']
    """
    return redirect(url_for('home.user_login', next=request.url))
