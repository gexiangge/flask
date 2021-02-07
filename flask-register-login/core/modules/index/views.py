# @Time    : 2020-11-02 19:48
# @Author  : 老赵
# @File    : views.py
from flask import jsonify, session, current_app, make_response

from core.models import UserLogin
from core.modules.index import index_blu
from core.utils.common import user_login_data, login_check
from core.utils.constants import PROJECT_FILE_DIR
from core.utils.status_code import response_code


@index_blu.route('/users')
@login_check
def users():
    # 如果 用户登陆之后才能访问，我们可以查看session中的值，发现有用户存在及处于登陆状态
    # # 获取用户编号
    # user_id = session.get("user_id")
    # print(user_id)
    # # 查询用户对象
    # user = None
    # if user_id:
    #     try:
    #         user = UserLogin.query.get(user_id)
    #     except Exception as e:
    #         current_app.logger.error(e)
    # if not user:
    #     return jsonify(response_code.user_not_exist)
    user = UserLogin.query.all()
    data = {
        'code': 1,
        'msg': '用户信息获取成功',
        'data': [i.to_dict() for i in user],
    }
    return jsonify(data)


@index_blu.route("/<re(r'(.+?).mp4$'):filename>")
def show_video(filename):
    video_path = PROJECT_FILE_DIR + filename
    video_data = open(video_path, "rb").read()
    response = make_response(video_data)
    response.headers['Content-Type'] = 'video/mp4'
    return response


@index_blu.route("/send/<mobile:mobile_num>")
def send_sms(mobile_num):
    return "send to %s" % mobile_num
