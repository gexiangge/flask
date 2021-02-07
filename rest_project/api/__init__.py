# @Time    : 2021-01-24 22:40
# @Author  : 老赵
# @File    : __init__.py.py
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from api.user import UserApi
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
# db = SQLAlchemy(app)


api = Api(app)
api.add_resource(UserApi, '/api/v1/user', '/user')

from api.book import book_blu
app.register_blueprint(book_blu)