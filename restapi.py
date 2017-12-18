from flask import Flask, request
from flask_restful import Resource, Api

from flask import jsonify
import requests

import main

app = Flask(__name__)
api = Api(app)


class Search(Resource):
    def get(self):
        search_str = request.args.get('str')
        from_ = request.args.get('from')
        size = request.args.get('size')
        sentiment = request.args.get('sentiment')

        # Parse from
        if from_ is None or int(from_) < 0:
            from_ = 0

        # Parse size
        if size is None or int(size) < 1:
            size = 100

        # Parse sentiment
        if sentiment is not None:
            if not(sentiment in ['n', 'p', 'v']):
                return requests.HTTPError(400)  # Wrong parameter send by client

        res = main.es_search(search_str, from_=from_, size=size, sentiment=sentiment)

        for hit in res['hits']['hits']:
            print(hit)

        return jsonify(res)


api.add_resource(Search, '/search')


if __name__ == '__main__':
    app.run(port=5002, debug=True)
    # Runs on http://127.0.0.1:5002/search?str=teststr