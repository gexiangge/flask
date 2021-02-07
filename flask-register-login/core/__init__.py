# @Time    : 2020-11-02 17:48
# @Author  : 老赵
# @File    : __init__.py.py
from flask import Flask, request, g, current_app, abort, jsonify
from flask_jwt_extended import JWTManager
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from config.config import Config, configs
from core.utils import constants
from core.utils.converter import RegexConverter, MobileConverter
from core.utils.log_utils import setup_log
from core.utils.status_code import response_code

db = SQLAlchemy()  # 创建SQLAlchemy对象
redis_store = None


def create_app(config_name):
    """创建app的工厂方法
    参数：根据参数选择不同的配置类
    """
    # 根据传入的config_name获取到对应的配置类
    config = configs[config_name]

    # 根据创建app时的配置环境，加载日志等级
    setup_log(config_name)

    app = Flask(__name__)

    app.config.from_object(config)  # 加载配置

    # 将自定义转换器添加到转换器字典中，并指定转换器使用时名字为: re
    app.url_map.converters['re'] = RegexConverter
    app.url_map.converters["mobile"] = MobileConverter

    # db = SQLAlchemy(app)  # 创建连接到MySQL数据库的对象
    db.init_app(app)

    global redis_store
    redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT,
                              decode_responses=True)  # 创建连接到redis数据库的对象

    # 创建Session对象,关联app，指定session数据存储在后端的位置
    Session(app)

    jwt = JWTManager(app)

    # 定义错误的处理方法
    @app.errorhandler(404)
    def handle_404_error(err):
        """
        自定义的处理错误方法
        :return:
        """
        # 这个函数的返回值会是前端用户看到的最终结果, 我们设置json格式返回
        # return "出现了404错误，错误信息：%s" % err
        return response_code.not_found

    @app.errorhandler(500)
    def internal_server_error(e):
        # return '服务器搬家了, 错误信息：', e
        return response_code.server_error

    @app.before_request
    def before_request():
        token = request.headers.get('token')
        user_id = redis_store.get('token:%s' % token)
        if user_id:
            from core.models import UserLogin
            g.current_user = UserLogin.query.get(user_id)
            g.token = token
            count = 0
            # 先从缓存里面查询请求次数
            try:
                count = redis_store.get("request_count:%s" % user_id) or 0
            except Exception as e:
                current_app.logger.error(e)

            if isinstance(count, str):
                count = int(count)

            # 如果次数大于10,直接不让用户再继续了
            if count >= 10:
                return jsonify(response_code.request_count_frequently)

            count += 1
            try:
                redis_store.set("request_count:%s" % user_id, count, constants.REQUEST_COUNT_REDIS_EXPIRES)

            except Exception as e:
                current_app.logger.error(e)

        # if not request.user_agent:
        #     return jsonify(response_code.no_user_agent)
        return

    # 注册首页蓝图对象
    from core.modules.index import index_blu
    app.register_blueprint(index_blu)

    # 注册passport蓝图对象
    from core.modules.passport import passport_blu
    app.register_blueprint(passport_blu)

    # 注册token_passport蓝图对象
    from core.modules.token_passport import token_passport_blu
    app.register_blueprint(token_passport_blu)

    # 注册jwt_passport蓝图对象
    from core.modules.jwt_passport import jwt_passport_blu
    app.register_blueprint(jwt_passport_blu)

    # 注册auth蓝图对象
    from core.modules.auth import auth_blu
    app.register_blueprint(auth_blu)

    return app
