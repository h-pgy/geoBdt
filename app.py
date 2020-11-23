from flask import Flask
from flask_restx import Resource, Api
from config import db_path
from models import db
from BdtApi.bdt_build import ApiBdtBuilder
from BdtApi.proj_errors import SQLNotFound, UnexpectedWebserviceResponse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app, version='1.0', title='GeoBDT Automático',
    description='GeoBDT - Boletim de Dados Técnicos Automático e Georreferenciado',
)

ns = api.namespace('BDT', description='Conjunto de endpoints que permitem consultar os dados do BDT')

@ns.errorhandler(SQLNotFound)
def handle_sql_not_found(e):

    return {'success' : False,
            'data' : [],
            'message' : str(e)}, 404

@ns.errorhandler(UnexpectedWebserviceResponse)
def handle_unexpected_resp(e):

    return {'success' : False,
            'data' : [],
            'message' : str(e)}, 500

def envelope(func):

    def wrapped(*args, **kwargs):

        resp = func(*args, **kwargs)

        enveloped = {'success' : True,
                     'message' : 'O resultado desta pesquisa possui apenas caráter indicativo e não exime da consulta '\
                                'formal aos órgãos competentes.',
                     'data' : resp}

        return enveloped

    return wrapped


def gerar_bdt(setor, quadra, lote=None, digito=None):

    lote=lote or '0001'
    digito = digito or '1'
    bdt = ApiBdtBuilder(setor, quadra, lote, digito)

    return bdt


@ns.route('/area_manancial/<string:setor>/<string:quadra>')
class manancial(Resource):

    @envelope
    def get(self, setor, quadra):
        bdt = gerar_bdt(setor, quadra)
        return bdt.area_manancial

@ns.route('/operacao_urbana/<string:setor>/<string:quadra>')
class operacao_urbana(Resource):

    @envelope
    def get(self,setor, quadra):
        bdt = gerar_bdt(setor, quadra)
        return bdt.operacao_urbana

@ns.route('/hidrografia/<string:setor>/<string:quadra>')
class hidrografia(Resource):

    @envelope
    def get(self,setor, quadra):
        bdt = gerar_bdt(setor, quadra)
        return bdt.hidrografia

@ns.route('/dis_dup/<string:setor>/<string:quadra>')
class dis_dup(Resource):

    @envelope
    def get(self,setor, quadra):
        bdt = gerar_bdt(setor, quadra)
        return bdt.dis_dup

@ns.route('/melhoramento_viario/<string:setor>/<string:quadra>')
class melhoramento_viario(Resource,):

    @envelope
    def get(self,setor, quadra):
        bdt = gerar_bdt(setor, quadra)
        return bdt.melhoramento_viario

@ns.route('/area_protecao_ambiental/<string:setor>/<string:quadra>')
class area_protecao_ambiental(Resource):

    @envelope
    def get(self,setor, quadra):
        bdt = gerar_bdt(setor, quadra)
        return bdt.area_protecao_ambiental

@ns.route('/restricao_geotecnica/<string:setor>/<string:quadra>')
class restricao_geotecnica(Resource):

    @envelope
    def get(self,setor, quadra):
        bdt = gerar_bdt(setor, quadra)
        return bdt.restricao_geotecnica

@ns.route('/historico_contaminacao/<string:setor>/<string:quadra>/<string:lote>')
class historico_contaminacao(Resource):

    @envelope
    def get(self,setor, quadra, lote):
        bdt = gerar_bdt(setor, quadra, lote)
        return bdt.historico_contaminacao

@ns.route('/tombamentos/<string:setor>/<string:quadra>/<string:lote>/<string:digito>')
class tombamentos(Resource):

    @envelope
    def get(self,setor, quadra, lote, digito):
        bdt = gerar_bdt(setor, quadra, lote, digito)
        return bdt.tombamentos


@ns.route('/zoneamento/<string:setor>/<string:quadra>/<string:lote>')
class zoneamento(Resource):

    @envelope
    def get(self,setor, quadra, lote):
        bdt = gerar_bdt(setor, quadra, lote)
        return bdt.zoneamento

@ns.route('/bdt/<string:sql>')
class bdt(Resource):

    def get(self, sql):
        sql, digito = tuple(sql.split('-'))
        setor, quadra, lote = tuple(sql.split('.'))

        bdt = gerar_bdt(setor, quadra, lote, digito)
        return {
           'bdt': {
                'Área de manancial' : bdt.area_manancial,
                'Operação Urbana' : bdt.operacao_urbana,
                'Hidrografia' : bdt.hidrografia,
                'DIS e DUP' : bdt.dis_dup,
                'Melhoramento Viário' : bdt.melhoramento_viario,
                'Área de Proteção Ambiental' : bdt.area_protecao_ambiental,
                'Restrição Geotécnica' : bdt.restricao_geotecnica,
                'Histórico de Contaminação' : bdt.historico_contaminacao,
                'Patrimônio Histórico' : bdt.tombamentos,
                'Zoneamento' : bdt.zoneamento
           }
        }

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0')