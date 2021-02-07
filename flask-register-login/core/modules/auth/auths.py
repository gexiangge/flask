# @Time    : 2020-11-04 10:50
# @Author  : 老赵
# @File    : auths.py
import datetime

import jwt
from flask import jsonify

from config.config import Config
from core.models import UserLogin
from core.utils.status_code import response_code
from core.utils.time_utils import datetime_to_stamp


class Auth(object):
    @staticmethod
    def encode_auth_token(user_id, login_time):
        """
        生成认证Token
        :param user_id: int
        :param login_time: int(timestamp)
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),
                'iat': datetime.datetime.utcnow(),
                'iss': 'zhao',
                'data': {
                    'id': user_id,
                    'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                Config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        try:
            # payload = jwt.decode(auth_token, Config.SECRET_KEY, leeway=datetime.timedelta(seconds=10))
            # 取消过期时间验证
            payload = jwt.decode(auth_token, Config.SECRET_KEY, options={'verify_exp': False})
            if 'data' in payload and 'id' in payload['data']:
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'

    def authenticate(self, mobile, password):
        """
        用户登录，登录成功返回token，写将登录时间写入数据库；登录失败返回失败原因
        :param password:
        :return: json
        """
        user = UserLogin.query.filter_by(mobile=mobile).first()
        if not user:
            return jsonify(response_code.user_not_exist)
        else:
            if user.check_password(password):
                login_time = datetime.datetime.now()
                user.last_login = login_time
                user.update()
                # 需要把登陆时间转化成时间戳的格式
                login_time_stamp = datetime_to_stamp(login_time)
                token = self.encode_auth_token(user.id, login_time_stamp)
                response_dict = response_code.success
                response_dict['token'] = token.decode()
                return jsonify(response_dict)
            else:
                return jsonify(response_code.password_not_fill)

    def identify(self, request):
        """
        用户鉴权
        :return: list
        """
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token_arr = auth_header.split(" ")
            if not auth_token_arr or auth_token_arr[0] != 'JWT' or len(auth_token_arr) != 2:
                return response_code.auth_header_error
            else:
                auth_token = auth_token_arr[1]
                payload = self.decode_auth_token(auth_token)
                if not isinstance(payload, str):
                    user_id = payload.get('data').get('id')
                    login_time = payload.get('data').get('login_time')
                    user = UserLogin.query.get(user_id)
                    if not user:
                        return response_code.user_not_exist
                    else:
                        if datetime_to_stamp(user.last_login) == login_time:
                            response_dict = response_code.success
                            response_dict['user_id'] = user.id
                            return response_dict
                        else:
                            return response_code.auth_token_change
                else:
                    return response_code.auth_token_payload_error
        else:
            return response_code.auth_token_not_exist
