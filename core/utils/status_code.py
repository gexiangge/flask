# @Time    : 2020-11-02 22:35
# @Author  : 老赵
# @File    : status_code.py


class ResponseCode(object):
    @property
    def success(self):
        return {'code': 200, 'msg': '请求成功'}

    @property
    def login_info_error(self):
        return {'code': 1001, 'msg': '用户名或者密码错误'}

    @property
    def password_not_fill(self):
        return {'code': 1002, 'msg': '密码信息填写完整'}

    @property
    def two_password_diff(self):
        return {'code': 1003, 'msg': '两次密码不一致'}

    @property
    def old_password_not_fill(self):
        return {'code': 1004, 'msg': '旧密码不正确'}

    @property
    def login_fail(self):
        return {'code': 1005, 'msg': '登录失败请联系管理员'}

    @property
    def password_reset_fail(self):
        return {'code': 1006, 'msg': '密码重置失败'}

    @property
    def user_not_exist(self):
        return {'code': 1007, 'msg': '用户不存在'}

    @property
    def import_csv_fail(self):
        return {'code': 1008, 'msg': '导入数据失败'}

    @property
    def import_csv_success(self):
        return {'code': 1009, 'msg': '导入数据成功'}

    @property
    def record_exist(self):
        return {'code': 1010, 'msg': '记录已存在'}

    @property
    def add_data_fail(self):
        return {'code': 1011, 'msg': '添加数据失败'}

    @property
    def update_data_fail(self):
        return {'code': 1012, 'msg': '修改数据失败'}

    @property
    def delete_data_fail(self):
        return {'code': 1013, 'msg': '删除数据失败'}

    @property
    def get_data_fail(self):
        return {'code': 1014, 'msg': '获取数据失败'}

    @property
    def request_version_not_exist(self):
        return {'code': 1015, 'msg': '请求的版本不存在'}

    @property
    def params_type_error(self):
        return {'code': 1016, 'msg': '参数类型错误'}

    @property
    def data_not_exist(self):
        return {'code': 1017, 'msg': '数据不存在'}

    @property
    def request_params_not_fill(self):
        return {'code': 1018, 'msg': '请求参数缺失'}

    @property
    def request_params_format_error(self):
        return {'code': 1019, 'msg': '请求参数格式错误'}

    @property
    def db_connect_error(self):
        return {'code': 1021, 'msg': "数据库连接失败"}

    @property
    def not_found(self):
        return {'code': 404, 'msg': 'HTTP 404 Not Found'}

    @property
    def bad_request(self):
        return {'code': 400, 'msg': 'HTTP 400 Bad Request'}

    @property
    def forbidden(self):
        return {'code': 403, 'msg': 'HTTP 403 Forbidden'}

    @property
    def params_wrong_values(self):
        return {'code': 1022, 'msg': '参数值超出规定范围'}

    @property
    def check_data_error(self):
        return {'code': 1023, 'msg': '验证数据错误'}

    @property
    def exception_db(self):
        return {'code': 1024, 'msg': '数据库操作异常'}

    @property
    def server_error(self):
        return {'code': 500, 'msg': '服务器端开小差了，大写的BUG😂😂😂'}

    @property
    def auth_header_error(self):
        return {'code': 1025, 'msg': '验证头信息有误'}

    @property
    def auth_token_change(self):
        return {'code': 1026, 'msg': 'Token已更改，请重新登录获取'}

    @property
    def auth_token_not_exist(self):
        return {'code': 1027, 'msg': '没有提供认证token'}

    @property
    def auth_token_payload_error(self):
        return {'code': 1028, 'msg': 'payload有误'}

    @property
    def request_count_frequently(self):
        return {'code': 1029, 'msg': '请求次数过于频繁，请稍后尝试'}

    @property
    def no_user_agent(self):
        return {'code': 1030, 'msg': '没有UA，如果是爬虫就低调点吧。。。'}


response_code = ResponseCode()
