# @Time    : 2020-11-03 20:09
# @Author  : 老赵
# @File    : __init__.py.py
from flask import Blueprint

jwt_passport_blu = Blueprint('jwt_passport', __name__, url_prefix='/jwt_passport')

from . import views