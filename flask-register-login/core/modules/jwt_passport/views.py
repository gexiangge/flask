# @Time    : 2020-11-03 20:09
# @Author  : 老赵
# @File    : views.py
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, create_access_token, jwt_refresh_token_required, \
    create_refresh_token, get_jwt_identity

from core.models import UserLogin
from core.modules.jwt_passport import jwt_passport_blu
from core.utils.status_code import response_code


@jwt_passport_blu.route('/login', methods=['POST'])
def login():
    # 1.获取参数
    dict_data = request.json
    mobile = dict_data.get("mobile")
    password = dict_data.get("password")

    # 2.校验参数
    if not all([mobile, password]):
        return jsonify(response_code.password_not_fill)

    # 3.通过手机号取出用户对象
    try:
        user = UserLogin.query.filter(UserLogin.mobile == mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(response_code.get_data_fail)

    # 4.判断用户对象是否存在
    if not user:
        return jsonify(response_code.user_not_exist)

    # 5.判断密码是否正确
    if not user.check_password(password):
        return jsonify(response_code.two_password_diff)

    ret = {
        'access_token': create_access_token(identity=mobile),
        'refresh_token': create_refresh_token(identity=mobile)
    }

    return jsonify(ret), 200


@jwt_passport_blu.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200


@jwt_passport_blu.route('/protected', methods=['GET'])
@jwt_required
def protected():
    mobile = get_jwt_identity()
    return jsonify(logged_in_as=mobile), 200
