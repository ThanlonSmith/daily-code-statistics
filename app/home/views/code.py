from .. import home
from flask import render_template


@home.route('/code/upload/')
def code_upload():

    return render_template('home/upload_code.html')


@home.route('/record/<int:id>/')
def commit_record(id=None):
    return render_template('home/commit_record.html')
