# @Time    : 2021-01-24 22:01
# @Author  : 老赵
# @File    : user.py
from api.libs.redprint import Redprint

api = Redprint('user')


@api.route('/')
def user_index():
    return 'user_index'


@api.route('/book')
def book():
    return 'book'
