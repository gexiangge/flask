# @Time    : 2021-01-24 22:01
# @Author  : 老赵
# @File    : admin.py


from api.libs.redprint import Redprint

api = Redprint('admin')


@api.route('/')
def admin_index():
    return 'admin_index'
