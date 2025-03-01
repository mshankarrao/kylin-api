import datetime
from flask import Flask, make_response, Response, jsonify, request, Blueprint
from flask_restx import Resource, Api, fields
from api.oracle_framework import OracleFramework
from api.errors import errors

app = Flask(__name__)
app.register_blueprint(errors)
api = Api(
    app,
    doc='/swagger',
    version='1.0.0',
    title='kylin-api',
    description='The API to provide the price feeds for the currency pairs from different sources(coingecko, coinbase, kraken, cryptowatch, etc)',
)

oracle_framework = OracleFramework()

@api.route('/prices', endpoint='prices')
@api.param('currency_pairs', 'the currency_pairs')
class PriceList(Resource):
    def get(self):
        currency_pairs = request.args['currency_pairs']
        prices = oracle_framework.get_prices(currency_pairs)
        return make_response(prices, 200)

@api.route('/health', endpoint='health')
class HealthList(Resource):
    def get(self):
        return Response("OK", status=200)


if __name__ == "__main__":
    app.run()
