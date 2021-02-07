# @Time    : 2020-11-03 17:09
# @Author  : 老赵
# @File    : views.py
import hashlib
import re
import time
from datetime import datetime

from flask import request, jsonify, current_app, g

from core import db, redis_store
from core.models import UserLogin
from core.modules.token_passport import token_passport_blu
from core.utils import constants
from core.utils.common import login_check
from core.utils.status_code import response_code


@token_passport_blu.route('/logout', methods=['POST'])
@login_check
def logout():
    """
    # 退出登陆(restful)
    # 请求路径: /passport/logout
    # 请求方式: POST
    # 请求参数: 无
    :return: code, msg
    """
    user_id = g.current_user.id
    token = g.token
    # 查询redis中的值  删除token相关信息
    try:
        redis_store.delete("user:%s" % user_id)
        redis_store.delete("token:%s" % token)

    except Exception as e:
        current_app.logger.error(e)
    # 返回响应
    return jsonify(response_code.success)


@token_passport_blu.route('/login', methods=['POST'])
def login():
    """
    # 登陆用户
    # 请求路径: /token_passport/login
    # 请求方式: POST
    # 请求参数: mobile,password
    # 返回值: code, msg, token

    1.获取参数
    2.校验参数
    3.通过手机号取出用户对象
    4.判断用户对象是否存在
    5.判断密码是否正确
    6.生成token
    7.存储token
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
        user_login = UserLogin.query.filter(UserLogin.mobile == mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(response_code.get_data_fail)

    # 4.判断用户对象是否存在
    if not user_login:
        return jsonify(response_code.user_not_exist)

    # 5.判断密码是否正确
    if not user_login.check_password(password):
        return jsonify(response_code.two_password_diff)

    # 生成token
    m = hashlib.md5()
    m.update(mobile.encode("utf8"))
    m.update(password.encode("utf8"))
    m.update(str(int(time.time())).encode("utf8"))
    token = m.hexdigest()

    user_id = user_login.id
    user_data = {
        "user_id": user_id,
        "mobile": user_login.mobile,
        "token": token
    }

    # 3.保存到redis
    try:
        pipeline = redis_store.pipeline()
        pipeline.hmset("user:%s" % user_id, user_data)  # user:1 存储用户信息
        pipeline.set("token:%s" % token, user_id)  # token:sd...sd 存储user_id
        pipeline.expire('token:%s' % token, constants.LOGIN_INFO_REDIS_EXPIRES)  # 设置token的有效期
        pipeline.execute()
    except Exception as e:
        current_app.logger.error(e)

    # 记录用户最后登陆时间
    user_login.last_login = datetime.now()

    # 保存到数据库
    try:
        db.session.add(user_login)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(response_code.add_data_fail)

    # 返回json
    response_dict = response_code.success
    response_dict['token'] = token
    return jsonify(response_dict)


@token_passport_blu.route('/register', methods=['POST'])
def register():
    """
    # 注册用户
    # 请求路径: /token_passport/register
    # 请求方式: POST
    # 请求参数: mobile, password
    # 返回值: code, msg

    1.获取参数
    2.校验参数(为空校验,手机号格式校验)
    3.创建用户对象,设置属性
    4.保存到数据库
    5.生成token
    6.保存redis，返回前端
    :return:
    """
    # 1.获取参数,
    dict_data = request.json
    mobile = dict_data.get("mobile")
    password = dict_data.get("password")

    # 2.校验参数(为空校验,手机号格式校验)
    if not all([mobile, password]):
        return jsonify(response_code.password_not_fill)

    # 2.1验证手机号格式
    if not re.match('1[3456789]\\d{9}', mobile):
        return jsonify(response_code.params_wrong_values)

    # 3.创建用户对象,设置属性
    user_info = UserLogin()
    user_info.mobile = mobile
    user_info.password = password

    # 4.保存到数据库
    try:
        db.session.add(user_info)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(response_code.add_data_fail)

    # 5. 生成token
    m = hashlib.md5()
    m.update(mobile.encode("utf8"))
    m.update(password.encode("utf8"))
    m.update(str(int(time.time())).encode("utf8"))
    token = m.hexdigest()

    user_id = user_info.id
    user_data = {
        "user_id": user_id,
        "mobile": mobile,
        "token": token
    }

    # 6.保存到redis
    try:
        pipeline = redis_store.pipeline()
        pipeline.hmset("user:%s" % user_id, user_data)  # user:1 存储用户信息
        pipeline.set("token:%s" % token, user_id)  # token:sd...sd 存储user_id
        pipeline.expire('token:%s' % token, constants.LOGIN_INFO_REDIS_EXPIRES)  # 设置token的有效期
        pipeline.execute()
    except Exception as e:
        current_app.logger.error(e)

    # 7.返回json
    response_code.success['token'] = token
    return jsonify(response_code.success)
