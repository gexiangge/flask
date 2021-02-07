# @Time    : 2020-11-04 11:37
# @Author  : 老赵
# @File    : time_utils.py
from datetime import datetime
import time


def string_to_date(string):
    """
    #把字符串转成date
    :param string:
    :return:
    """
    return datetime.strptime(string, "%Y-%m-%d")


def string_to_datetime(string):
    """
    #把字符串转成datetime
    :param string:
    :return:
    """
    return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")


def date_to_time(timestring):
    """
    date转时间戳
    :param timestring:
    :return:
    """
    return time.mktime(time.strptime(timestring, '%Y-%m-%d'))


def datetime_to_time(timestring):
    """
    datetime转时间戳
    :param timestring:
    :return:
    """
    return time.mktime(time.strptime(timestring, '%Y-%m-%d %H:%M:%S'))


def datetime_to_stamp(datetime):
    """
    datetime转时间戳
    :param datetime:
    :return: int-stamp
    """
    return int(time.mktime(datetime.timetuple()))


if __name__ == '__main__':
    pass
