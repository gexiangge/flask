# @Time    : 2021-01-24 22:38
# @Author  : 老赵
# @File    : manager.py
from flask_script import Manager

from api import app

manager = Manager(app)

if __name__ == '__main__':
    manager.run()