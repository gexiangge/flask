# @Time    : 2021-01-24 21:59
# @Author  : 老赵
# @File    : __init__.py.py
from flask import Blueprint

from api.v1 import user, admin


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)
    user.api.register(bp_v1, url_prefix='/user')
    admin.api.register(bp_v1, url_prefix='/admin')
    return bp_v1
