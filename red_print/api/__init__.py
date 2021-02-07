# @Time    : 2021-01-24 21:57
# @Author  : 老赵
# @File    : __init__.py.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object(Config)

from api.v1 import create_blueprint_v1

app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')