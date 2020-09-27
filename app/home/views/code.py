from .decoration import login_wrapper
import datetime
import os
import uuid

from .. import home
from flask import render_template, request, flash, session
from app.utils import db_helper


def check_upload():
    """
    判断今天的代码是否上传
    :return:
    """
    ctime = datetime.date.today()  # 当前日期
    data = db_helper.fetchone('select id from record where ctime = %s and user_id = %s',
                              (ctime, session['user_info']['id']))
    return data


def get_code_line(target_path):
    """
    4. 遍历目录下的所有文件，计算有效代码行数
    :param target_path:
    :return:
    """
    # for item in os.listdir(target_path):
    #     print(item)
    # for item in os.walk(target_path):
    #     # 每一个item是一个元组，每一个元组有三个元素，分别是当前路径、当前路径下所有文件夹、当前路径下的所有文件
    #      print(item)  # ('files/79d81a3d-455f-4124-ba24-7d7b8a990c4a/keymaps', [], ['Default Proper Redo.xml'])
    sum_num = 0
    for base_path, folder_list, file_list in os.walk(target_path):
        for file_name in file_list:
            file_path = os.path.join(base_path, file_name)
            # print(file_path)  # files/b39a2b87-69b3-4094-942a-58103e70b8a6/options/databaseDrivers.xml
            file_ext = file_path.rsplit('.', 1)
            if len(file_ext) != 2:
                continue
            if file_ext[1] != 'py':
                continue
            file_num = 0
            with open(file_path, 'rb') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith(b'#'):
                        continue
                    file_num += 1
            # print(file_num, file_path)  # 每一个文件行数
            sum_num += file_num
            return sum_num


@home.route('/code/upload/', methods=['POST', 'GET'])
@login_wrapper
def code_upload():
    if request.method == "POST":
        if check_upload():
            flash('今天的代码已经上传了！', 'error')
            return render_template('home/upload_code.html')
        file_obj = request.files.get('code')  # <FileStorage: '' ('application/octet-stream')>,把上传的东西方内存了
        # print(file_obj.filename)  # 上传的文件名(带扩展名)
        # print(file_obj.stream)  # 文件的内容被封装到对象中
        """
        1.检查上传文件的后缀名
        """
        filename_ext = file_obj.filename.rsplit('.', maxsplit=1)  # 元组
        msg = str()
        if len(filename_ext) != 2:
            msg = '请上传压缩文件!'
            return render_template('home/upload_code.html', msg=msg)
        if filename_ext[1] != 'zip':
            msg = '请上传后缀名为zip的文件'
            return render_template('home/upload_code.html', msg=msg)

        """
        2.接受用户上传的文件并写入到本地
        """
        if not os.path.exists('files'):
            os.mkdir('files')  # 项目目录下，非app目录下
        file_path = os.path.join('files', file_obj.filename)
        file_obj.save(file_path)  # save的本质是：从file_obj.stream中读取内容写入到文件
        """
        3.解压zip文件
        """
        import shutil
        target_path = os.path.join('files', str(uuid.uuid4()))  # 允许上传的文件名相同
        # print(target_path) # files/549fb0e2-924c-460d-a993-935fcc8e3274
        # 通过open打开压缩文件，读取内容再进行解压
        shutil._unpack_zipfile(file_path, target_path)

        # 2和3步合并，接受用户上传的文件，并解压至指定目录
        # import shutil
        # shutil._unpack_zipfile(file_obj.stream, r'/home/thanlon/PycharmProjects/code_count/files')
        """
        5. 持久化到数据库
        """
        ctime = datetime.date.today()
        db_helper.insert('insert record(line,ctime,user_id) values(%s,%s,%s)',
                         (get_code_line(target_path), ctime, session['user_info']['id']))
        flash('上传成功！', 'ok')
    return render_template('home/upload_code.html')


@home.route('/record/<int:id>/<int:page>/')
@login_wrapper
def commit_record(id=None, page=None):
    print(session)
    """
    <SecureCookieSession {'user_info': {'id': 1, 'nickname': 'thanlon', 'pwd': 'ea48576f30be1669971699c09ad05c94', 'user': 'thanlon'}}>
    """
    print(session['user_info'])
    """
    {'id': 1, 'nickname': 'thanlon', 'pwd': 'ea48576f30be1669971699c09ad05c94', 'user': 'thanlon'}
    """
    print(session['user_info'].get('id', None))  # 通过页码传用户的id和直接从session获取一样
    record_list = db_helper.fetch_all(
        'select id,line,ctime from record  where user_id = %s order by ctime asc limit 0,5', (id,))
    print(record_list)
    data_list, time_list = list(), list()
    for row in record_list:
        data_list.append(row['line'])
        time_list.append(float(row['ctime'].strftime("%m.%d")))  # datetime类型转换成字符串
    print(data_list)
    print(time_list)
    """
    [135, 897, 1032, 374, 678]
    [9.26, 9.25, 9.27, 9.24, 9.23]
    """
    return render_template('home/commit_record.html', data_list=data_list, time_list=time_list, record_list=record_list)
