# @Time    : 2020-11-02 21:32
# @Author  : 老赵
# @File    : models.py
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

from core import db


class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间


class UserLogin(BaseModel, db.Model):
    """用户登陆表"""
    __tablename__ = "user_login"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 用户id
    mobile = db.Column(db.String(16), unique=True, nullable=False)  # 手机号
    # password = db.Column(db.String(128), nullable=False)  # 密码
    password_hash = db.Column(db.String(128), nullable=False)  # 密码
    last_login = db.Column(db.DateTime, default=datetime.now)  # 最后一次登录时间

    # passpord方法通过property修饰之后,可以当成属性形式调用 设置访问密码的方法,并用装饰器@property设置为属性,调用时不用加括号
    @property
    def password(self):
        raise AttributeError("当前属性不可读")  # _password

    # 设置set方法  设置加密的方法,传入密码,对类属性进行操作
    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    # 加密密码
    def jiami_secret(self, value):
        return generate_password_hash(value)

    # 设置验证密码的方法  传入密文,明文到check_password_hash方法中,如果验证正确返回true,否则返回false
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        res_dict = {
            'id': self.id,
            'mobile': self.mobile,
            'last_login': self.last_login,
        }
        return res_dict

    def add(self, user):
        db.session.add(user)
        return session_commit()

    def update(self):
        return session_commit()

    def delete(self, id):
        self.query.filter_by(id=id).delete()
        return session_commit()


def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return reason
