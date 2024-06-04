# @Time    : 2020-11-04 11:51
# @Author  : 老赵
# @File    : views.py
import re

from flask import request, jsonify

from core.models import UserLogin
from core.modules.auth import auth_blu
from core.modules.auth.auths import Auth
from core.utils.status_code import response_code


@auth_blu.route('/register', methods=['POST'])
def register():
    """
    用户注册
    :return: json
    """
    data_dict = request.json
    mobile = data_dict.get('mobile')
    password = data_dict.get('password')

    # 2.校验参数(为空校验,手机号格式校验)
    if not all([mobile, password]):
        return jsonify(response_code.request_params_missed)

    # 2.1验证手机号格式
    if not re.match('1[356789]\\d{9}', mobile):
        return jsonify(response_code.request_params_format_error)

    user = UserLogin()
    user.mobile = mobile
    user.password = password

    error_reason = user.add(user)  # 数据库添加

    if not error_reason:
        return jsonify(response_code.success)
    else:
        response_code.user_not_exist['sql_error'] = error_reason
        return jsonify(response_code.user_not_exist)


@auth_blu.route('/login', methods=['POST'])
def login():
    """
    用户登录
    :return: json
    """
    data_dict = request.json
    mobile = data_dict.get('mobile')
    password = data_dict.get('password')

    # 2.校验参数(为空校验,手机号格式校验)
    if not all([mobile, password]):
        return jsonify(response_code.request_params_missed)

    # 2.1验证手机号格式
    if not re.match('1[356789]\\d{9}', mobile):
        return jsonify(response_code.request_params_format_error)

    return Auth().authenticate(mobile, password)


@auth_blu.route('/user', methods=['GET'])
def user():
    """
    获取用户信息
    :return: json
    """
    result = Auth().identify(request)

    if result['code'] == 200:
        user = UserLogin.query.get(result.get('user_id'))
        user_dict = user.to_dict()
        response_code.success['data'] = user_dict
        return jsonify(response_code.success)
    else:
        return jsonify(result)
