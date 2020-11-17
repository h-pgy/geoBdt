from .get_api_data import ApiDataGetter
from .proj_errors import SQLNotFound, UnexpectedWebserviceResponse
from .helpers import build_response, parsear_zoneamento


class ApiBdtBuilder:

    def __init__(self, setor, quadra, lote, digito, data_getter = None):

        if data_getter is None:
            self.api = ApiDataGetter()
        self.setor = setor
        self.quadra = quadra
        self.lote = lote
        self.digito = digito or '1'

    @property
    def area_manancial(self):

        resp = self.api.consult_mananc_prox(self.setor, self.quadra)
        try:
            if resp['Resultado'] == 'SIM':

                return [
                    build_response('Incide área de manancial',
                                   'Identifica se a quadra em que se situa o projeto está localizada em área de manancial',
                                   True
                                   ),
                    build_response('Nome',
                                   'Identificação do manancial em que a quadra incide',
                                   resp['Nome']
                                   )
                ]
            elif resp['Resultado'] == 'NÃO':
                return build_response('Incide área de manancial',
                                   'Identifica se a quadra em que se situa o projeto está localizada em área de manancial',
                                   False
                                   )

            elif resp['Resultado'] is None:
                raise SQLNotFound(f'A quadra não foi encontrada: {self.setor}.{self.quadra}')

            else:
                raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')
        except KeyError:
            raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')

    @property
    def operacao_urbana(self):

        resp = self.api.consult_operacao_urb(self.setor, self.quadra)
        try:
            if resp['Resultado'] == 'SIM':

                return [
                    build_response('Incide operação urbana',
                                   'Se há incidência de operação urbana no projeto',
                                   True),
                    build_response('Nome da Operação Urbana',
                                   'Nome da operação urbana que incide no projeto',
                                   resp['Nome']),
                    build_response('Setor',
                                   'Identificação do setor da operação urbana que incide no projeto',
                                   resp['Setor'])
                ]

            elif resp['Resultado'] == 'NÃO':

                return build_response('Incide operação urbana',
                                   'Se há incidência de operação urbana no projeto',
                                   False)

            elif resp['Resultado'] is None:

                raise SQLNotFound(f'A quadra não foi encontrada: {self.setor}.{self.quadra}')

            else:
                raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')
        except KeyError:
            raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')

    @property
    def hidrografia(self):

        resp = self.api.prox_hidrografia(self.setor, self.quadra)

        if resp == 'SIM':
            return build_response('Próximo a hidrografia',
                                  'Indica se o projeto está próximo a corpo de água/hidrografia',
                                  True)
        elif resp == 'NÃO':
            return build_response('Próximo a hidrografia',
                                  'Indica se o projeto está próximo a corpo de água/hidrografia',
                                  False)
        elif resp is None:

            raise SQLNotFound(f'A quadra não foi encontrada: {self.setor}.{self.quadra}')

        else:
            raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')

    @property
    def dis_dup(self):

        resp = self.api.consult_dup_dis(self.setor, self.quadra)
        try:
            if resp['Resultado'] == 'SIM':
                return [
                    build_response('Incidência de DUP ou DIS',
                                   'Indica se há incidência de Decreto de Interesse Social ou Decreto de Utilidade Pública'
                                   ' sobre a quadra em que se localiza o projeto',
                                   True),
                    build_response('Tipo da Norma',
                                   'Indica se o decreto é de "interesse público" (DIS) ou "utilidade pública" (DUP)',
                                   resp['Tipo']
                                   ),
                    build_response('Número',
                                   'Numeração identificadora da norma',
                                   resp['Numero']),
                    build_response('Ano',
                                   'Ano de publicação da norma',
                                   int(resp['Data'][:4]))
                ]

            elif resp['Resultado'] == 'NÃO':
                return build_response('Incidência de DUP ou DIS',
                                   'Indica se há incidência de Decreto de Interesse Social ou Decreto de Utilidade Pública'
                                   ' sobre a quadra em que se localiza o projeto',
                                   False)

            elif resp['Resultado'] is None:

                raise SQLNotFound(f'A quadra não foi encontrada: {self.setor}.{self.quadra}')

            else:
                raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')
        except KeyError:
            raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')

    @property
    def melhoramento_viario(self):
        #to do: maybe reduce the size of this funcion with a helper

        resp = self.api.consult_melhor_viario(self.setor, self.quadra)
        try:
            lista_melhor = resp['ArrayOfMelhoramentoViarioMelhoramentoViario']
        except KeyError:
            raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')

        if not lista_melhor:
            raise SQLNotFound(f'A quadra não foi encontrada: {self.setor}.{self.quadra}')
        elif type(lista_melhor) is not list:
            raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')
        #then there's a result that should be parsed
        else:
            full_resp = []
            for obj in lista_melhor:
                if obj['Resultado'] == 'NÃO':
                    obj_resp = [
                        build_response('Incidência de melhoramento viário',
                                       'Indica se há incidência de melhoramento viário ou faixa não edificável'
                                       'na quadra em que se situa o projeto',
                                       False),
                        build_response('Tipo de melhoramento',
                                       'Identifica o tipo de melhoramento (viário ou faixa não edificável)',
                                       obj['MelhoramentoFaixa'])
                    ]
                    full_resp.append(obj_resp)
                elif obj['Resultado'] == 'SIM':
                    obj_resp = [
                        build_response('Incidência de melhoramento viário',
                                       'Indica se há incidência de melhoramento viário ou faixa não edificável'
                                       'na quadra em que se situa o projeto',
                                       True),
                        build_response('Tipo de melhoramento',
                                       'Identifica o tipo de melhoramento (viário ou faixa não edificável)',
                                       obj['MelhoramentoFaixa']),
                        build_response('Ano da norma',
                                       'Ano de publicação da norma que fundamenta o melhoramento viário',
                                       obj['AnoLeiMelhoramentoVigente']),
                        build_response('Tipo da norma',
                                       'Identifica o tipo da norma que fundamenta o melhoramento viário',
                                       obj['IdentificadorTipoNorma']),

                    ]

                    full_resp.append(obj_resp)

            return full_resp

    @property
    def area_protecao_ambiental(self):

        resp = self.api.consult_protec_ambient(self.setor, self.quadra)

        if resp is None:

            raise SQLNotFound(f'A quadra não foi encontrada: {self.setor}.{self.quadra}')
        elif resp == 'NÃO':

            return build_response('Área de proteção ambiental',
                                  'Identifica se a quadra em que se encontra o projeto se localiza'
                                  ' em área de proteção ambiental',
                                  False)
        elif resp == 'SIM':

            return build_response('Área de proteção ambiental',
                                  'Identifica se a quadra em que se encontra o projeto se localiza'
                                  ' em área de proteção ambiental',
                                  True)
        else:
            raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')

    @property
    def restricao_geotecnica(self):

        resp = self.api.consult_restr_geotec(self.setor, self.quadra)
        try:
            if resp['Resultado'] is None:
                raise SQLNotFound(f'A quadra não foi encontrada: {self.setor}.{self.quadra}')

            elif resp['Resultado'] == 'NÃO':
                return build_response('Restrição Geotécnica',
                                      'Indica se a quadra onde se situa o projeto '
                                      'está localizada em área de restrição geotécnica',
                                      False)
            elif resp['Resultado'] == 'SIM':
                return [build_response('Restrição Geotécnica',
                                      'Indica se a quadra onde se situa o projeto '
                                      'está localizada em área de restrição geotécnica',
                                      True),
                        build_response('Área de restrição geotécnica',
                                       'Identificação da área de restrição geotécnica'
                                       ' em que se encontra o projeto',
                                       resp['NomeLocal']),
                        build_response('Regulamentação',
                                       'Normativa que regulamenta a área de restrição geotécnica identificada',
                                       resp['TextoRegulamentacao'])
                ]

            else:
                raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')
        except KeyError:
            raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')

    @property
    def historico_contaminacao(self):

        resp = self.api.consult_processo_contaminacao(self.setor, self.quadra, self.lote)

        #a webservice nao diferencia SQL invalido de SQL que nao possui processos!
        try:
            if resp['Processos'] is None:
                return build_response('Processos de contaminação',
                                      'Identifica se há processos de contaminação para o SQL solicitado. '
                                      'ATENÇÃO: a webservice não valida se o SQL solicitado é válido',
                                      False)
            elif resp['Processos']:
                full_resp = []
                for proc in resp['Processos']['ProcessoContaminacao_Retorno']:
                    proc_resp = [build_response('Contaminante',
                                                'Identifica o contaminante avaliado no processo',
                                                proc['Contaminante']),
                                 build_response('Etapa do processo',
                                                'Identifica a etapa em que o processo de contaminação se encontra',
                                                proc['Etapa']),
                                 build_response('Restrição de uso',
                                                'Descreve se há alguma restrição de uso no imóvel devido à contaminação',
                                                proc['RestricaoUso']),
                                 build_response('Situação da área',
                                                'Identifica qual a situação atual da área. '
                                                'Por exemplo: se ainda está contaminada, se já foi recuperada etc..',
                                                proc['Situacao'])
                                 ]

                    full_resp.append(proc_resp)

                return full_resp
            else:
                raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')
        except KeyError:
            raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')

    @property
    def tombamentos(self):

        resp = self.api.consult_tombamentos(self.setor, self.quadra, self.lote, self.digito)

        #a webservice nao diferencia SQL invalido de SQL que nao possui processos!

        if resp is None:
            return build_response('Tombamentos/Patrimônio Histórico',
                                  'Identifica se o imóvel em que se situa o projeto está protegido pelo Patrimônio Histórico. '
                                  'ATENÇÃO: a webservice não valida se o SQL solicitado é válido',
                                  False)
        elif type(resp) is list:

            tombamentos = []
            for tomb_resp in resp:
                tomb = [
                    build_response('Código do nível de preservação',
                                   'Código que identifica o nível de preservação do imóvel pelo patrimônio histórico.',
                                   tomb_resp['CodigoNivelPreservacao']),
                    build_response('Descrição da preservação',
                                   'Descreve o tipo de preservação do imóvel pelo patrimônio histórico',
                                   tomb_resp['NivelPreservacao']),
                    build_response('Data de atualização',
                                   'Data da última atualização das informações sobre o tombamento',
                                   tomb_resp['DataAtualizacao'][:10]),
                    build_response('Data de cadastro',
                                   'Data do cadastro do tombamento',
                                   tomb_resp['DataCadastro'][:10]),
                    build_response('Endereço do tombamento',
                                   'Endereço como consta no processo de tombamento',
                                   tomb_resp['Endereco']),
                    build_response('Observação',
                                   'Observação acrescentada pelos técnicos',
                                   tomb_resp['Observacao'])
                ]

                tombamentos.append(tomb)

            return tombamentos

        else:
            raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')

    @property
    def zoneamento(self):

        resp = self.api.obter_zoneamento(self.setor, self.quadra, self.lote)
        try:
            if resp['Codigo'] == 4:
                raise SQLNotFound(f'O lota não foi encontrado: {self.setor}.{self.quadra}.{self.lote}')
            elif resp['Codigo'] == 0:

                zoneamento_formatado = []
                zoneamento = parsear_zoneamento(resp)
                for zona in zoneamento:
                    if zona['TipoZoneamento'] == 'Zona de Uso':

                        formated = [
                            build_response('Sigla',
                                           'Sigla da Zona de Uso',
                                           zona['SiglaZonaUso']),
                            build_response('Descrição',
                                           'Descrição da zona de uso',
                                           zona['DescricaoZonaUso']),
                            build_response('Legislação',
                                           'Legislação que cria/regulamenta a zona de uso',
                                           zona['Legislacao'])
                        ]

                    elif zona['TipoZoneamento'] == 'Setores da Macroárea de Estruturação Metropolitana':

                        formated = [
                            build_response('Setor',
                                           'Nome do setor da MEM',
                                           zona['NomeSetor']),
                            build_response('Código',
                                           'Código do setor da MEM',
                                           zona['CodigoSetor'])
                        ]

                    elif zona['TipoZoneamento'] == 'Quota Ambiental':

                        formated = [
                            build_response('PA',
                                           'Perímetro de Qualificação Ambiental',
                                           zona['Perímetro de Qualificação Ambiental'])
                        ]

                    elif zona['TipoZoneamento'] == 'Perímetro de Incentivo ao Desenvolvimento Econômico':
                        formated = [
                            build_response('PI',
                                           'Perímetro de Incentivo ao Desenvolvimento Econômico',
                                           zona['CodigoPerimetro'])
                        ]


                    zoneamento_formatado.append(formated)

                return zoneamento_formatado

            else:
                raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')
        except KeyError:
            raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')

















