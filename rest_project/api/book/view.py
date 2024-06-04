from flask_restful import Resource


class BookApi(Resource):
    def get(self):
        return 'books'

    def post(self):
        pass

    def put(self):
        pass
