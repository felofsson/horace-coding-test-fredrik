from flask import Flask, request
from flask_restful import Resource, Api
# from sqlalchemy import create_engine
# from json import dumps
# from flask.ext.jsonpify import jsonpify

app = Flask(__name__)
api = Api(app)


class Search(Resource):
    def get(self):
        search_str = request.args.get('str')

        print(search_str)

        return search_str


api.add_resource(Search, '/search')


if __name__ == '__main__':
    app.run(port=5002)