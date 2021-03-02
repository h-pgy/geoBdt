from .client_creating import create_client
from .api_logging import log_request

class ApiDataGetter:

    def __init__(self, client = None, log_requests = False, bdt_id = None):

        self.client = client
        self.log_requests = log_requests
        self.bdt_id = bdt_id or 'NaoRegistrado'

    @create_client()
    @log_request
    def obter_zoneamento(self, setor, quadra, lote, client):

        resp = client.service['ObterZoneamento.v1'](cdSetor=setor,
                                                    cdQuadra=quadra,
                                                    cdLote=lote)
        return resp

    @create_client()
    @log_request
    def obter_param_construtivo(self, zona, client):

        resp = client.service['ObterParametrosConstrutivos.v1'](zona=zona)

        return resp

    @create_client()
    @log_request
    def consult_dup_dis(self, setor, quadra, client):

        resp = client.service['ConsultarDupDisPorSQL.v1'](setor, quadra)

        return resp

    @create_client()
    @log_request
    def prox_hidrografia(self, setor, quadra, client):

        resp = client.service['ConsultarHidrografiaPorSQ.v1'](setor, quadra)

        return resp

    @create_client()
    @log_request
    def consult_mananc_prox(self, setor, quadra, client):

        resp = client.service['ConsultarManancialPorSQ.v1'](setor, quadra)

        return resp

    @create_client()
    @log_request
    def consult_melhor_viario(self, setor, quadra, client):

        resp = client.service['ConsultarMelhoramentoViarioPorSQ.v1'](setor, quadra)

        return resp

    @create_client()
    @log_request
    def consult_operacao_urb(self, setor, quadra, client):

        resp = client.service['ConsultarOperacaoUrbanaPorSQ.v1'](setor, quadra)

        return resp

    @create_client()
    @log_request
    def consult_protec_ambient(self, setor, quadra, client):

        resp = client.service['ConsultarProtecaoAmbientalPorSQ.v1'](setor, quadra)

        return resp

    @create_client()
    @log_request
    def consult_restr_geotec(self, setor, quadra, client):

        resp = client.service['ConsultarRestricaoGeotecnicaPorSQ.v1'](setor, quadra)

        return resp

    @create_client()
    @log_request
    def consult_protec_voo(self, setor, quadra, client):

        resp = client.service['ConsultarProtecaoVooPorSQ.v1'](setor, quadra)

        return resp

    @create_client()
    @log_request
    def consult_area_espec_trafego(self, setor, quadra, lote, client):

        resp = client.service['ObterAreaEspecialTrafego.v1'](setor, quadra, lote)

        return resp

    @create_client()
    @log_request
    def consult_processo_contaminacao(self, setor, quadra, lote, client):

        resp = client.service['ConsultarProcessoContaminacao.v1'](setor, quadra, lote)

        return resp

    @create_client()
    @log_request
    def consult_tombamentos(self, setor, quadra, lote, digito, client):

        resp = client.service['ConsultarTombamentos.v1'](setor, quadra, lote, digito)

        return resp

    @create_client()
    @log_request
    def consult_imovel_por_sql(self, setor, quadra, lote, digito, client):

        str_sql = ''.join([setor, quadra, lote, digito])
        resp = client.service['ObterLocalPorSQL.v1'](str_sql, 'S')

        return resp

    @create_client()
    @log_request
    def consult_logradouro_por_cep(self, cep, client):

        resp = client.service['ConsultarLogradouroPorCEP.v1'](cep, 1)

        return resp

    @create_client()
    @log_request
    def consult_ccm(self, cpf_ou_cnpj, numero, client):

        cpf_ou_cnpj = cpf_ou_cnpj.lower().strip()

        if  cpf_ou_cnpj == 'cnpj':

            resp = client.service['ConsultarDadosEstabelecimento.v1'](dadosEntrada = {'CNPJ' : numero})

            return resp

        elif cpf_ou_cnpj == 'cpf':

            resp = client.service['ConsultarDadosEstabelecimento.v1'](dadosEntrada = {'CPF' : numero})

            return resp

        else:
            return {}
