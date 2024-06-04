from flask_migrate import MigrateCommand, Migrate
from flask_restful import Api
from flask_script import Manager

from app import app, db
from resources.book import BookCRUD, Books
from resources.user import UserRegister, UserLogin

manager = Manager(app)
Migrate(app, db)
manager.add_command("db", MigrateCommand)

from models.user import UserModel
from models.book import BookModel

api = Api(app)

api.add_resource(UserRegister, '/passport/register', endpoint='register')
api.add_resource(UserLogin, '/passport/login', endpoint='login')
api.add_resource(Books, '/books', endpoint='books')
api.add_resource(BookCRUD, '/books/book', endpoint='book')

if __name__ == '__main__':
    manager.run()
