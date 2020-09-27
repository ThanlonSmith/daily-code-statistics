from settings import Config
import pymysql


def fetchone(sql, args):
    '''
    获取单条数据
    :param sql: 执行的sql语句
    :param args: 其它参数
    :return:没有值返回空元组
    '''
    conn = Config.POOL.connection()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql, args)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


def fetch_all(sql, args):
    '''
    获取所有数据
    :param sql: 执行的sql语句
    :param args: 其它参数
    :return:没有值返回空元组
    '''
    conn = Config.POOL.connection()
    # cursor = conn.cursor()  # ((1, 'thanlon', 'thanlon'), (2, 'kiku', 'kiku'))
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    """
    [{'id': 1, 'user': 'thanlon', 'nickname': 'thanlon'}, {'id': 2, 'user': 'kiku', 'nickname': 'kiku'}]
    """
    cursor.execute(sql, args)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def insert(sql, args):
    '''
    向数据库中插入数据
    :param sql: 执行的sql语句
    :param args: 其它参数
    :return: 受影响的行数
    '''
    conn = Config.POOL.connection()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    row = cursor.execute(sql, args)
    conn.commit()
    cursor.close()
    conn.close()
    return row
