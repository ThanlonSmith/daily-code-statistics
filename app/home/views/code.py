from .. import home
from flask import render_template


@home.route('/code/upload/')
def code_upload():
    return render_template('home/upload_code.html')
