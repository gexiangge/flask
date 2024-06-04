import logging

import redis


class Config:
    """工程配置信息"""
    # 开启调试模式
    DEBUG = True

    # 让jsonify返回的json串支持中文显示
    JSON_AS_ASCII = False

    # 项目秘钥：session,还有其他的一些签名算法会用
    SECRET_KEY = 'e\x94I\xe0\xb2L\xab\x01\xcf"\xc5\xe1j=\xf4\xcb\xc2\x8a\xfd\x14\xe13JZ'

    # 配置MySQL数据库连接信息:真实开发中，要使用mysql数据库的真实IP
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@127.0.0.1:3306/restful"
    # 不去追踪数据库的修改，节省开销
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 配置redis数据库:因为redis模块不是flask的扩展，所以就不会自动的从config中读取配置信息，只能自己读取
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # flask_session的配置信息
    SESSION_TYPE = "redis"  # 指定 session 保存到 redis 中
    SESSION_USE_SIGNER = True  # 让 cookie 中的 session_id 被加密签名处理
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # 使用 redis 的实例
    PERMANENT_SESSION_LIFETIME = 24 * 60 * 60  # session 的有效期，单位是秒

    # 默认日志等级
    LOG_LEVEL = logging.DEBUG


class DevelopementConfig(Config):
    """开发模式下的配置"""
    pass


class ProductionConfig(Config):
    """生产模式下的配置"""
    DEBUG = False
    LOG_LEVEL = logging.ERROR


class UnittestConfig(Config):
    """测试环境"""
    TESTING = True


# 定义配置字典
configs = {
    "development": DevelopementConfig,
    "production": ProductionConfig,
    "test": UnittestConfig,
}
