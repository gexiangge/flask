from flask import session
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mobile = db.Column(db.String(64), unique=True, nullable=False)
    nickname = db.Column(db.String(64), unique=False, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, mobile, nickname, password):
        self.mobile = mobile
        self.nickname = nickname
        self.password_hash = generate_password_hash(password)

    def add_user(self):
        try:
            db.session.add(self)
            db.session.commit()
            return 0, "success", self._get_user_info()
        except Exception as e:
            return -1, str(e), self._get_user_info()
        finally:
            db.session.close()

    @classmethod
    def login_user(cls, mobile, password):
        try:
            _user = cls.query.filter_by(mobile=mobile).first()
            if _user is None:
                return -3, "user does not exist", dict()
            else:
                if not check_password_hash(_user.password_hash, password):
                    return -2, "password incorrect", _user._get_user_info()
                else:
                    session["user"] = _user.id
                    return 0, "login successful", _user._get_user_info()
        except Exception as e:
            return -1, str(e), dict()

    def _get_user_info(self):
        return {
            "mobile": self.mobile,
            "nickname": self.nickname,
            "password_hash": self.password_hash
        }
