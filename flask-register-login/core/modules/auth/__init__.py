# @Time    : 2020-11-04 10:49
# @Author  : 老赵
# @File    : __init__.py.py


from flask import Blueprint

auth_blu = Blueprint('auth', __name__, url_prefix='/auth')

from . import views