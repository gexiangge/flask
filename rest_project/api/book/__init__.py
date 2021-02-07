# @Time    : 2021-01-24 22:47
# @Author  : 老赵
# @File    : __init__.py.py
from flask import Blueprint
from flask_restful import Api

from api.book.view import BookApi

book_blu = Blueprint('book', __name__, url_prefix='/book')

api = Api(book_blu)

api.add_resource(BookApi, '/book')
