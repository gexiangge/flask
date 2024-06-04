# @Time    : 2020-11-02 21:27
# @Author  : 老赵
# @File    : views.py
import re
from datetime import datetime

from flask import request, jsonify, current_app, session

from core import db
from core.models import UserLogin
from core.modules.passport import passport_blu
from core.utils.status_code import response_code


@passport_blu.route('/logout', methods=['POST'])
def logout():
    """
    # 退出登陆(restful)
    # 请求路径: /passport/logout
    # 请求方式: POST
    # 请求参数: 无
    # 返回值: code, msg
    :return:
    """
    # 清除session中的数据
    # session.clear()
    session.pop("user_id", "")
    session.pop("mobile", "")

    # 返回响应
    return jsonify(response_code.success)


@passport_blu.route('/login', methods=['POST'])
def login():
    """
    # 登陆用户
    # 请求路径: /passport/login
    # 请求方式: POST
    # 请求参数: mobile,password
    # 返回值: code, msg

    1.获取参数
    2.校验参数
    3.通过手机号取出用户对象
    4.判断用户对象是否存在
    5.判断密码是否正确
    6.记录用户登陆状态
    7.返回json
    :return:
    """
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

    # 6.记录用户登陆状态
    session["user_id"] = user.id
    session["mobile"] = user.mobile

    # 记录用户最后登陆时间
    user.last_login = datetime.now()

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(response_code.update_data_fail)

    # 7.返回前端页面
    return jsonify(response_code.success)


@passport_blu.route('/register', methods=['POST'])
def register():
    """
    url_for('passport.register')
    # 请求路径: /passport/register
    # 请求方式: POST
    # 请求参数: mobile, password
    # 返回值: code, msg

    获取参数
    校验参数(为空校验,手机号格式校验)
    创建用户对象,设置属性
    保存到数据库
    返回json
    :return:
    """
    # 1.获取参数,三种方式获取到字典,先转成json,再次转成字典/ get_json / json
    # 第一种:
    # json_data = request.data
    # dict_data = json.loads(json_data)
    # 第二种:
    # dict_data =  request.get_json()
    # 第三种:
    dict_data = request.json

    mobile = dict_data.get("mobile")
    password = dict_data.get("password")

    # 2.校验参数(为空校验,手机号格式校验)
    if not all([mobile, password]):
        return jsonify(response_code.request_params_not_fill)

    # 2.1验证手机号格式
    if not re.match('1[356789]\\d{9}', mobile):
        return jsonify(response_code.request_params_format_error)

    # 3.创建用户对象,设置属性
    user = UserLogin()
    user.mobile = mobile
    # 普通方式
    # user.password_hash = jia_mi_fangfa(password)
    # 使用@propert装饰之后,可以直接当成属性的形式来调用
    user.password = password

    # user.password_hash = user.jiami_secret(password)

    # 4.保存到数据库
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(response_code.add_data_fail)

    # 8.返回前端页面
    return jsonify(response_code.success)
