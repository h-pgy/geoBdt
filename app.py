import datetime
import json
import os
from flask import Flask, request
from flask_restx import Resource, Api, fields
from models import db, BdtLog, BdtRequestLog
from BdtApi.bdt_build import ApiBdtBuilder
from BdtApi.proj_errors import (SQLNotFound,
                                UnexpectedWebserviceResponse,
                                CEPNotFound,
                                BDTNotFound,
                                ZonaUsoNotFound,
                                ParametroInvalido,
                                CPFouCNPJNotFound)
from BdtApi.helpers import build_response

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['db_path']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app, version='1.0', title='GeoBDT Automático',
    description='GeoBDT - Boletim de Dados Técnicos Automático e Georreferenciado',
)

ns = api.namespace('BDT', description='Conjunto de endpoints que permitem consultar os dados do BDT')

bdt = api.model('BDT', {
    'setor' : fields.String,
    'quadra'  : fields.String,
    'lote' : fields.String,
    'digito' : fields.String,
})

@ns.errorhandler(SQLNotFound)
def handle_sql_not_found(e):

    return {'success' : False,
            'data' : [],
            'message' : str(e)}, 404

@ns.errorhandler(CEPNotFound)
def handle_cep_not_found(e):

    return {'success' : False,
            'data' : [],
            'message' : str(e)}, 404

@ns.errorhandler(ZonaUsoNotFound)
def handle_zona_not_found(e):

    return {'success' : False,
            'data' : [],
            'message' : str(e)}, 404

@ns.errorhandler(BDTNotFound)
def handle_bdt_not_found(e):

    return {'success' : False,
            'data' : [],
            'message' : str(e)}, 404

@ns.errorhandler(CPFouCNPJNotFound)
def handle_cpf_cnpj_not_found(e):

    return {'success' : False,
            'data' : [],
            'message' : str(e)}, 404

@ns.errorhandler(ParametroInvalido)
def handle_parametro_invalido(e):

    return {'success' : False,
            'data' : [],
            'message' : str(e)}, 500

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


def gerar_bdt(setor, quadra, lote=None, digito=None, bdt_id = None):

    lote=lote or '0001'
    digito = digito or '1'
    bdt = ApiBdtBuilder(setor, quadra, lote, digito, bdt_id)

    return bdt


@ns.route('/area_manancial/<string:sq>')
class manancial(Resource):

    @envelope
    def get(self, sq):
        if request.args.get('sq'):
            sq_list = request.args.get('sq').split(',')
            response = []
            for sq in sq_list:
                setor, quadra = tuple(sq.split('.'))
                bdt = gerar_bdt(setor, quadra)
                response.append({ 'label': sq, 'description': sq, 'value': bdt.area_manancial })
            return response
        else:
            setor, quadra = tuple(sq.split('.'))
            bdt = gerar_bdt(setor, quadra)
            return bdt.area_manancial


@ns.route('/operacao_urbana/<string:sq>')
class operacao_urbana(Resource):

    @envelope
    def get(self, sq):
        if request.args.get('sq'):
            sq_list = request.args.get('sq').split(',')
            response = []
            for sq in sq_list:
                setor, quadra = tuple(sq.split('.'))
                bdt = gerar_bdt(setor, quadra)
                response.append({ 'label': sq, 'description': sq, 'value': bdt.operacao_urbana })
            return response
        else:
            setor, quadra = tuple(sq.split('.'))
            bdt = gerar_bdt(setor, quadra)
            return bdt.operacao_urbana

@ns.route('/hidrografia/<string:sq>')
class hidrografia(Resource):

    @envelope
    def get(self, sq):
        if request.args.get('sq'):
            sq_list = request.args.get('sq').split(',')
            response = []
            for sq in sq_list:
                setor, quadra = tuple(sq.split('.'))
                bdt = gerar_bdt(setor, quadra)
                response.append({ 'label': sq, 'description': sq, 'value': bdt.hidrografia })
            return response
        else:
            setor, quadra = tuple(sq.split('.'))
            bdt = gerar_bdt(setor, quadra)
            return bdt.hidrografia


@ns.route('/dis_dup/<string:sq>')
class dis_dup(Resource):

    @envelope
    def get(self, sq):
        if request.args.get('sq'):
            sq_list = request.args.get('sq').split(',')
            response = []
            for sq in sq_list:
                setor, quadra = tuple(sq.split('.'))
                bdt = gerar_bdt(setor, quadra)
                response.append({ 'label': sq, 'description': sq, 'value': bdt.dis_dup })
            return response
        else:
            setor, quadra = tuple(sq.split('.'))
            bdt = gerar_bdt(setor, quadra)
            return bdt.dis_dup

@ns.route('/melhoramento_viario/<string:sq>')
class melhoramento_viario(Resource):

    @envelope
    def get(self, sq):
        if request.args.get('sq'):
            sq_list = request.args.get('sq').split(',')
            response = []
            for sq in sq_list:
                setor, quadra = tuple(sq.split('.'))
                bdt = gerar_bdt(setor, quadra)
                response.append({ 'label': sq, 'description': sq, 'value': bdt.melhoramento_viario })
            return response
        else:
            setor, quadra = tuple(sq.split('.'))
            bdt = gerar_bdt(setor, quadra)
            return bdt.melhoramento_viario

@ns.route('/faixa_nao_edificavel/<string:sq>')
class faixa_nao_edificante(Resource):

    @envelope
    def get(self, sq):
        if request.args.get('sq'):
            sq_list = request.args.get('sq').split(',')
            response = []
            for sq in sq_list:
                setor, quadra = tuple(sq.split('.'))
                bdt = gerar_bdt(setor, quadra)
                response.append({ 'label': sq, 'description': sq, 'value': bdt.faixa_nao_edificavel })
            return response
        else:
            setor, quadra = tuple(sq.split('.'))
            bdt = gerar_bdt(setor, quadra)
            return bdt.faixa_nao_edificavel

@ns.route('/area_protecao_ambiental/<string:sq>')
class area_protecao_ambiental(Resource):

    @envelope
    def get(self, sq):
        if request.args.get('sq'):
            sq_list = request.args.get('sq').split(',')
            response = []
            for sq in sq_list:
                setor, quadra = tuple(sq.split('.'))
                bdt = gerar_bdt(setor, quadra)
                response.append({ 'label': sq, 'description': sq, 'value': bdt.area_protecao_ambiental })
            return response
        else:
            setor, quadra = tuple(sq.split('.'))
            bdt = gerar_bdt(setor, quadra)
            return bdt.area_protecao_ambiental

@ns.route('/restricao_geotecnica/<string:sq>')
class restricao_geotecnica(Resource):

    @envelope
    def get(self, sq):
        if request.args.get('sq'):
            sq_list = request.args.get('sq').split(',')
            response = []
            for sq in sq_list:
                setor, quadra = tuple(sq.split('.'))
                bdt = gerar_bdt(setor, quadra)
                response.append({ 'label': sq, 'description': sq, 'value': bdt.restricao_geotecnica })
            return response
        else:
            setor, quadra = tuple(sq.split('.'))
            bdt = gerar_bdt(setor, quadra)
            return bdt.restricao_geotecnica

@ns.route('/historico_contaminacao/<string:sql>')
class historico_contaminacao(Resource):

    @envelope
    def get(self, sql):
        if request.args.get('sql'):
            sql_list = request.args.get('sql').split(',')
            response = []
            for sql in sql_list:
                setor, quadra, lote = tuple(sql.split('.'))
                bdt = gerar_bdt(setor, quadra, lote)
                response.append({ 'label': sql, 'description': sql, 'value': bdt.historico_contaminacao })
            return response
        else:
            setor, quadra, lote = tuple(sql.split('.'))
            bdt = gerar_bdt(setor, quadra, lote)
            return bdt.historico_contaminacao


@ns.route('/tombamentos/<string:sql>')
class tombamentos(Resource):

    @envelope
    def get(self, sql):
        if request.args.get('sql'):
            sql_list = request.args.get('sql').split(',')
            response = []
            for sql in sql_list:
                sql, digito = tuple(sql.split('-'))
                setor, quadra, lote = tuple(sql.split('.'))
                bdt = gerar_bdt(setor, quadra, lote, digito)
                response.append({ 'label': sql, 'description': sql, 'value': bdt.tombamentos })
            return response
        else:
            sql, digito = tuple(sql.split('-'))
            setor, quadra, lote = tuple(sql.split('.'))
            bdt = gerar_bdt(setor, quadra, lote, digito)
            return bdt.tombamentos


@ns.route('/zoneamento/<string:sql>')
class zoneamento(Resource):

    @envelope
    def get(self, sql):
        if request.args.get('sql'):
            sql_list = request.args.get('sql').split(',')
            response = []
            for sql in sql_list:
                setor, quadra, lote = tuple(sql.split('.'))
                bdt = gerar_bdt(setor, quadra, lote)
                response.append({ 'label': sql, 'description': sql, 'value': bdt.zoneamento })
            return response
        else:
            setor, quadra, lote = tuple(sql.split('.'))
            bdt = gerar_bdt(setor, quadra, lote)
            return bdt.zoneamento

@ns.route('/busca_logradouro_por_cep/<string:cep>')
class busca_cep(Resource):

    @envelope
    def get(self,cep):
        bdt = gerar_bdt(None, None) #não precisa desses dados aqui
        return bdt.logradouro_por_cep(cep)

@ns.route('/parametros_construtivos_HIS/<string:sql>')
class param_constru_his(Resource):

    @envelope
    def get(self, sql):
        setor, quadra, lote = tuple(sql.split('.'))

        bdt = gerar_bdt(setor, quadra, lote)

        return bdt.param_constru_his

@ns.route('/taxa_permeabilidade_HIS/<string:sql>')
class tx_permeab_his(Resource):

    @envelope
    def get(self, sql):
        setor, quadra, lote = tuple(sql.split('.'))

        bdt = gerar_bdt(setor, quadra, lote)

        return bdt.tx_permeab_his

@ns.route('/empreendimento_aceito/<string:sql>/<string:tipo_empreendimento>')
class empreendimento_aceito(Resource):

    @envelope
    def get(self, sql, tipo_empreendimento):
        setor, quadra, lote = tuple(sql.split('.'))

        bdt = gerar_bdt(setor, quadra, lote)

        return bdt.zona_uso_aceita_his_ou_hmp(tipo_empreendimento)


@ns.route('/zona_uso_permite_declaratorio/<string:sql>')
class permite_declaratorio(Resource):

    @envelope
    def get(self, sql):
        setor, quadra, lote = tuple(sql.split('.'))

        bdt = gerar_bdt(setor, quadra, lote)

        return bdt.zona_uso_permite_his_declaratorio


@ns.route('/dados_endereco_iptu/<string:sql>')
class endereco_iptu(Resource):

    @envelope
    def get(self, sql):
        if request.args.get('sql'):
            sql_list = request.args.get('sql').split(',')
            response = []
            for sql in sql_list:
                sql, digito = tuple(sql.split('-'))
                setor, quadra, lote = tuple(sql.split('.'))
                bdt = gerar_bdt(setor, quadra, lote, digito)
                response.append({ 'label': sql, 'description': sql, 'value': bdt.dados_lograouro_iptu })
            return response
        else:
            sql, digito = tuple(sql.split('-'))
            setor, quadra, lote = tuple(sql.split('.'))
            bdt = gerar_bdt(setor, quadra, lote, digito)
            return bdt.dados_lograouro_iptu


@ns.route('/subprefeitura/<string:sql>')
class subprefeitura(Resource):

    @envelope
    def get(self, sql):
        setor, quadra, lote = tuple(sql.split('.'))
        bdt = gerar_bdt(setor, quadra, lote)

        return bdt.subprefeitura

@ns.route('/ccm_ativo/<string:cpf_ou_cnpj>/<string:numero>')
class endereco_iptu(Resource):

    @envelope
    def get(self, cpf_ou_cnpj, numero):
        bdt = gerar_bdt(None, None)

        return bdt.ccm_ativo(cpf_ou_cnpj, numero)

@ns.route('/bdt/<string:sql>')
class bdt(Resource):

    @envelope
    def get(self, sql):
        sql, digito = tuple(sql.split('-'))
        setor, quadra, lote = tuple(sql.split('.'))
        bdt = gerar_bdt(setor, quadra, lote)
        data = {
            'bdt': [
                build_response('Área de manancial',
                               'Área de manancial',
                               bdt.area_manancial if isinstance(bdt.area_manancial, list) else [bdt.area_manancial]
                ),
                build_response('Operação Urbana',
                               'Operação Urbana',
                               bdt.operacao_urbana if isinstance(bdt.operacao_urbana, list) else [bdt.operacao_urbana]
                ),
                build_response('Hidrografia',
                               'Hidrografia',
                               bdt.hidrografia if isinstance(bdt.hidrografia, list) else [bdt.hidrografia]
                ),
                build_response('DIS e DUP',
                               'DIS e DUP',
                               bdt.dis_dup if isinstance(bdt.dis_dup, list) else [bdt.dis_dup]
                ),
                build_response('Melhoramento Viário',
                               'Melhoramento Viário',
                               bdt.melhoramento_viario if isinstance(bdt.melhoramento_viario, list) else [bdt.melhoramento_viario]
                ),
                build_response('Faixa Não Edificável',
                               'Faixa Não Edificável',
                               bdt.faixa_nao_edificavel if isinstance(bdt.faixa_nao_edificavel, list) else [bdt.faixa_nao_edificavel]
                ),
                build_response('Área de Proteção Ambiental',
                               'Área de Proteção Ambiental',
                               bdt.area_protecao_ambiental if isinstance(bdt.area_protecao_ambiental, list) else [bdt.area_protecao_ambiental]
                ),
                build_response('Restrição Geotécnica',
                               'Restrição Geotécnica',
                               bdt.restricao_geotecnica if isinstance(bdt.restricao_geotecnica, list) else [bdt.restricao_geotecnica]
                ),
                build_response('Histórico de Contaminação',
                               'Histórico de Contaminação',
                               bdt.historico_contaminacao if isinstance(bdt.historico_contaminacao, list) else [bdt.historico_contaminacao]
                ),
                build_response('Patrimônio Histórico',
                               'Patrimônio Histórico',
                                bdt.tombamentos if isinstance(bdt.tombamentos, list) else [bdt.tombamentos]
                ),
                build_response('Zoneamento',
                               'Zoneamento',
                               bdt.zoneamento if isinstance(bdt.zoneamento, list) else [bdt.zoneamento])
            ]
        }
        return data
    

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0')
