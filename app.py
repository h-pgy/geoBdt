from flask import Flask
from flask_restx import Resource, Api
from BdtApi.bdt_build import ApiBdtBuilder

app = Flask(__name__)
api = Api(app, version='0.1', title='GeoBDT Mock API',
    description='Mock API para o GeoBDT',
)

ns = api.namespace('BDT', description='Endpoint para gerar o BDT')

def gerar_bdt(setor, quadra, lote=None, digito=None):

    lote=lote or '0001'
    digito = digito or '1'
    bdt = ApiBdtBuilder(setor, quadra, lote, digito)

    return bdt


@ns.route('/bdt/<string:sql>')
class bdt(Resource):

    def get(self, sql):
        sql, digito = tuple(sql.split('-'))
        setor, quadra, lote = tuple(sql.split('.'))

        bdt = gerar_bdt(setor, quadra, lote, digito)
        return {
           'bdt': [
                bdt.area_manancial,
                bdt.operacao_urbana,
                bdt.hidrografia,
                bdt.dis_dup,
                bdt.melhoramento_viario,
                bdt.area_protecao_ambiental,
                bdt.restricao_geotecnica,
                bdt.historico_contaminacao,
                bdt.tombamentos,
            ]
        }


@ns.route('/area_manancial/<string:setor>/<string:quadra>')
class manancial(Resource):

    def get(self, setor, quadra):
        bdt = gerar_bdt(setor, quadra)
        return bdt.area_manancial

@ns.route('/operacao_urbana/<string:setor>/<string:quadra>')
class operacao_urbana(Resource):

    def get(self,setor, quadra):
        bdt = gerar_bdt(setor, quadra)
        return bdt.operacao_urbana

@ns.route('/hidrografia/<string:setor>/<string:quadra>')
class hidrografia(Resource):

    def get(self,setor, quadra):
        bdt = gerar_bdt(setor, quadra)
        return bdt.hidrografia

@ns.route('/dis_dup/<string:setor>/<string:quadra>')
class dis_dup(Resource):

    def get(self,setor, quadra):
        bdt = gerar_bdt(setor, quadra)
        return bdt.dis_dup

@ns.route('/melhoramento_viario/<string:setor>/<string:quadra>')
class melhoramento_viario(Resource,):

    def get(self,setor, quadra):
        bdt = gerar_bdt(setor, quadra)
        return bdt.melhoramento_viario

@ns.route('/area_protecao_ambiental/<string:setor>/<string:quadra>')
class area_protecao_ambiental(Resource):

    def get(self,setor, quadra):
        bdt = gerar_bdt(setor, quadra)
        return bdt.area_protecao_ambiental

@ns.route('/restricao_geotecnica/<string:setor>/<string:quadra>')
class restricao_geotecnica(Resource):

    def get(self,setor, quadra):
        bdt = gerar_bdt(setor, quadra)
        return bdt.restricao_geotecnica

@ns.route('/historico_contaminacao/<string:setor>/<string:quadra>/<string:lote>')
class historico_contaminacao(Resource):

    def get(self,setor, quadra, lote):
        bdt = gerar_bdt(setor, quadra, lote)
        return bdt.historico_contaminacao

@ns.route('/tombamentos/<string:setor>/<string:quadra>/<string:lote>/<string:digito>')
class tombamentos(Resource):

    def get(self,setor, quadra, lote, digito):
        bdt = gerar_bdt(setor, quadra, lote, digito)
        return bdt.tombamentos


if __name__ == '__main__':
    app.run(debug=True)
