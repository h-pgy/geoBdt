from flask import Flask
from flask_restx import Resource, Api
from random import choice
import json

app = Flask(__name__)
api = Api(app, version='0.1', title='GeoBDT Mock API',
    description='Mock API para o GeoBDT',
)

ns = api.namespace('BDT', description='Endpoint para gerar o BDT')

def bdt_aleatorio():

    with open('data/bdts_json.json') as f:
        t = f.read()

    return choice(json.loads(t))

@ns.route('/geoBdt')
class GeoBdt(Resource):
    def post(self):

        return bdt_aleatorio()

    def get(self):

        return bdt_aleatorio()


if __name__ == '__main__':
    app.run(debug=True)