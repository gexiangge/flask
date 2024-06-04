from flask import request
from flask_restful import Resource, reqparse

from common.return_data import compose_return_data
from models.book import BookModel, BookStatus


class Books(Resource):
    def get(self):
        """
        get all books
        :return:
        """
        code, msg, books_data = BookModel.get_all_books()
        return compose_return_data(books_data, code, msg)


class BookCRUD(Resource):
    def post(self):
        """
        add new book
        :return:
        """
        j_data = request.get_json()
        _book = BookModel(j_data['name'], j_data['category'], j_data['price'], BookModel.get_login_user(), BookStatus.active)
        code, msg, book_data = _book.add_book()
        return compose_return_data(book_data, code, msg)

    def get(self):
        """
        get book by id
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument('book_id')
        args = parser.parse_args()

        book_id = args.get('book_id')
        code, msg, book_data = BookModel.get_book_by_id(book_id)
        return compose_return_data(book_data, code, msg)

    def delete(self):
        """
        delete book by id
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument('book_id')
        args = parser.parse_args()

        book_id = args.get('book_id')
        code, msg, book_data = BookModel.del_book_by_id(book_id)
        return compose_return_data(book_data, code, msg)

    def patch(self):
        """
        update books by given name and category
        :return:
        """
        j_data = request.get_json()
        code, msg, book_data = BookModel.update_book(j_data["name"], j_data["category"], j_data["price"])
        return compose_return_data(book_data, code, msg)
