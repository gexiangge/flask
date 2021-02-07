# @Time    : 2020-11-02 19:47
# @Author  : 老赵
# @File    : __init__.py.py
from flask import Blueprint

index_blu = Blueprint('index', __name__)

from . import views