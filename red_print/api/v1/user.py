from api.libs.redprint import Redprint

api = Redprint('user')


@api.route('/')
def user_index():
    return 'user_index'


@api.route('/book')
def book():
    return 'book'
