# @Time    : 2021-01-24 21:56
# @Author  : 老赵
# @File    : mangaer.py
from flask_script import Manager

from api import app

manager = Manager(app)

if __name__ == '__main__':
    manager.run()
