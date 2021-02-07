# @Time    : 2020-11-03 11:08
# @Author  : 老赵
# @File    : common.py
from functools import wraps

from flask import session, current_app, g, jsonify, request

from core import redis_store
from core.utils.status_code import response_code


def login_check(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('token')
        if not token:
            return jsonify(response_code.user_not_exist)

        user_id = redis_store.get('token:%s' % token)
        if not user_id or token != redis_store.hget('user:%s' % user_id, 'token'):
            return jsonify(response_code.check_data_error)

        return f(*args, **kwargs)

    return decorator


def user_login_data(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        # 获取用户编号
        user_id = session.get("user_id")
        # 查询用户对象
        user = None
        if user_id:
            try:
                from core.models import UserLogin
                user = UserLogin.query.get(user_id)
            except Exception as e:
                current_app.logger.error(e)

        # 使用g对象保存
        g.user = user
        # 如果用户不存在，返回用户不存在的json
        if not user:
            return jsonify(response_code.user_not_exist)

        return view_func(*args, **kwargs)

    return wrapper
