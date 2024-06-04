# @Time    : 2020-11-03 17:06
# @Author  : 老赵
# @File    : __init__.py.py

from flask import Blueprint

token_passport_blu = Blueprint('token_passport', __name__, url_prefix='/token_passport')

from . import views