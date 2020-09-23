from flask import Flask
from flask_restx import Resource, Api
from os import listdir
from random import choice

app = Flask(__name__)
api = Api(app, version='0.1', title='GeoBDT Mock API',
    description='Mock API para o GeoBDT',
)

ns = api.namespace('BDT', description='Endpoint para gerar o BDT')

def bdt_aleatorio():

    file = choice(['data/' + file for file in listdir('data')])

    with open(file) as f:
        t = f.read()

    return t

@ns.route('/geoBdt')
class GeoBdt(Resource):
    def post(self):

        return bdt_aleatorio()


if __name__ == '__main__':
    app.run(debug=True)