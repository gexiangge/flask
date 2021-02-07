from flask import request
from flask_restful import Resource

from common.return_data import compose_return_data
from models.user import UserModel


class UserRegister(Resource):
    def post(self):
        """
        register new user
        :return:
        """
        j_data = request.get_json()
        _user = UserModel(j_data['mobile'], j_data['nickname'], j_data['password'])
        code, msg, user_data = _user.add_user()
        return compose_return_data(user_data, code, msg)


class UserLogin(Resource):
    def post(self):
        """
        user login
        :return:
        """
        j_data = request.get_json()
        mobile, password = j_data['mobile'], j_data['password']
        code, msg, user_data = UserModel.login_user(mobile, password)
        return compose_return_data(user_data, code, msg)
