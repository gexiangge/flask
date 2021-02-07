# @Time    : 2021-01-24 22:49
# @Author  : 老赵
# @File    : view.py
from flask_restful import Resource


class BookApi(Resource):
    def get(self):
        return 'books'

    def post(self):
        pass

    def put(self):
        pass
