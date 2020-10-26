from .client_creating import create_client

class ApiDataGetter:

    def __init__(self, client = None):

        self.client = client

    @create_client()
    def obter_zoneamento(self, setor, quadra, lote, client):

        resp = client.service['ObterZoneamento.v1'](cdSetor=setor,
                                                    cdQuadra=quadra,
                                                    cdLote=lote)
        return resp

    @create_client()
    def obter_param_construtivo(self, zona, client):

        resp = client.service['ObterParametrosConstrutivos.v1'](zona=zona)

        return resp

    @create_client()
    def consult_dup_dis(self, setor, quadra, client):

        resp = client.service['ConsultarDupDisPorSQL.v1'](setor, quadra)

        return resp

    @create_client()
    def prox_hidrografia(self, setor, quadra, client):

        resp = client.service['ConsultarHidrografiaPorSQ.v1'](setor, quadra)

        return resp

    @create_client()
    def consult_mananc_prox(self, setor, quadra, client):

        resp = client.service['ConsultarManancialPorSQ.v1'](setor, quadra)

        return resp

    @create_client()
    def consult_melhor_viario(self, setor, quadra, client):

        resp = client.service['ConsultarMelhoramentoViarioPorSQ.v1'](setor, quadra)

        return resp

    @create_client()
    def consult_operacao_urb(self, setor, quadra, client):

        resp = client.service['ConsultarOperacaoUrbanaPorSQ.v1'](setor, quadra)

        return resp

    @create_client()
    def consult_protec_ambient(self, setor, quadra, client):

        resp = client.service['ConsultarProtecaoAmbientalPorSQ.v1'](setor, quadra)

        return resp

    @create_client()
    def consult_restr_geotec(self, setor, quadra, client):

        resp = client.service['ConsultarRestricaoGeotecnicaPorSQ.v1'](setor, quadra)

        return resp

    @create_client()
    def consult_protec_voo(self, setor, quadra, client):

        resp = client.service['ConsultarProtecaoVooPorSQ.v1'](setor, quadra)

        return resp

    @create_client()
    def consult_area_espec_trafego(self, setor, quadra, lote, client):

        resp = client.service['ObterAreaEspecialTrafego.v1'](setor, quadra, lote)

        return resp

    @create_client()
    def consult_processo_contaminacao(self, setor, quadra, lote, client):

        resp = client.service['ConsultarProcessoContaminacao.v1'](setor, quadra, lote)

        return resp

    @create_client()
    def consult_tombamentos(self, setor, quadra, lote, digito, client):

        resp = client.service['ConsultarTombamentos.v1'](setor, quadra, lote, digito)

        return resp