# @Time    : 2020-11-02 21:26
# @Author  : 老赵
# @File    : __init__.py.py
from flask import Blueprint

passport_blu = Blueprint('passport', __name__, url_prefix='/passport')

from . import views