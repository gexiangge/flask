import enum

from flask import session

from app import db


class BookStatus(enum.Enum):
    deleted = 0
    active = 1


class BookModel(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=False, nullable=False)
    category = db.Column(db.String(64), unique=False, nullable=False)
    price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.Enum(BookStatus))

    def __init__(self, name, category, price, user_id, status):
        self.name = name
        self.category = category
        self.price = price
        self.user_id = user_id
        self.status = status

    @classmethod
    def get_all_books(cls):
        if not cls.get_login_user():
            return -1, "no user login", list()
        try:
            _books = cls.query.all()
            book_list = list()
            for _book in _books:
                book_list.append(_book._get_book_info())
            return 0, "success", book_list
        except Exception as e:
            return -1, str(e), list()

    @classmethod
    def get_book_by_id(cls, book_id):
        if not cls.get_login_user():
            return -1, "no user login", dict()
        try:
            _book = cls.query.get(book_id)
            if _book:
                return 0, "success", _book._get_book_info()
            else:
                return -1, f"no book with ID {book_id}", dict()
        except Exception as e:
            return -1, str(e), dict()

    @classmethod
    def del_book_by_id(cls, book_id):
        if not cls.get_login_user():
            return -1, "no user login", dict()
        try:
            _book = cls.query.get(book_id)
            if _book:
                _book.status = BookStatus.deleted
                db.session.commit()
                return 0, "success", _book._get_book_info()
            else:
                return -1, f"no book with ID {book_id}", dict()
        except Exception as e:
            return -1, str(e), dict()
        finally:
            db.session.close()

    @classmethod
    def update_book(cls, name, category, price):
        if not cls.get_login_user():
            return -1, "no user login", dict()
        try:
            _books = cls.query.filter_by(name=name, category=category).all()
            if not _books:
                return -1, "no books matching condition", list()
            else:
                book_data = list()
                user_ids = list()
                for _book in _books:
                    _book.price = price
                    user_ids.append(_book.user_id)
                    book_data.append(_book._get_book_info())
                login_user_id = cls.get_login_user()
                if False in map(lambda x: x == login_user_id, user_ids):
                    return -1, f"current login user (id {login_user_id}) has no permission to update books", book_data
                else:
                    db.session.commit()
                    return 0, "success", book_data
        except Exception as e:
            return -1, str(e), list()
        finally:
            db.session.close()

    def add_book(self):
        if not self.user_id:
            return -1, "no user login", self._get_book_info()
        try:
            db.session.add(self)
            db.session.commit()
            return 0, "success", self._get_book_info()
        except Exception as e:
            return -1, str(e), self._get_book_info()
        finally:
            db.session.close()

    @classmethod
    def get_login_user(cls):
        return session['user'] if 'user' in session else ''

    def _get_book_info(self):
        return {
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "user_id": self.user_id,
            "status": str(self.status)
        }
