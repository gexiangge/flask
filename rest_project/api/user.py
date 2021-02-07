# @Time    : 2021-01-24 22:41
# @Author  : 老赵
# @File    : user.py
from flask_restful import Resource, fields, marshal_with


class UserApi(Resource):
    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'age': fields.String,
    }

    @marshal_with(resource_fields)
    def get(self):
        # users = User.query.all()
        return 'users'

    def post(self):
        pass


