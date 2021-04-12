from zeep.exceptions import Fault
from zeep.helpers import serialize_object
from .get_api_data import ApiDataGetter
from .proj_errors import SQLNotFound, UnexpectedWebserviceResponse, CEPNotFound, ZonaUsoNotFound, ParametroInvalido, CPFouCNPJNotFound
from .helpers import build_response, pegar_dados_zoneamento, dados_endereco_iptu, detalhes_tombamento, pegar_subprefeitura
from .zon_his_especifico import param_constru_his, tx_permeab_his, checar_tipologia_empreendimento, zona_uso_permite_declaratorio


class ApiBdtBuilder:

    def __init__(self, setor, quadra, lote, digito, bdt_id = None, log_requests = True, data_getter = None):

        if data_getter is None:
            self.api = ApiDataGetter(log_requests = log_requests, bdt_id = bdt_id)
        self.id = bdt_id or 'NaoRegistrado'
        self.setor = setor
        self.quadra = quadra
        self.lote = lote
        self.digito = digito

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
                if obj['Resultado'] == 'NÃO' and obj['MelhoramentoFaixa']=="MELHORAMENTO VIÁRIO":
                    obj_resp = [
                        build_response('Incidência de melhoramento viário',
                                       'Indica se há incidência de melhoramento viário ou faixa não edificável'
                                       'na quadra em que se situa o projeto',
                                       False)
                    ]
                    full_resp.append(obj_resp)
                elif obj['Resultado'] == 'SIM' and obj['MelhoramentoFaixa']=="MELHORAMENTO VIÁRIO":
                    obj_resp = [
                        build_response('Incidência de melhoramento viário',
                                       'Indica se há incidência de melhoramento viário'
                                       'na quadra em que se situa o projeto',
                                       True),
                        build_response('Ano da norma',
                                       'Ano de publicação da norma que fundamenta o melhoramento viário',
                                       obj['AnoLeiMelhoramentoVigente']),
                        build_response('Tipo da norma',
                                       'Identifica o tipo da norma que fundamenta o melhoramento viário',
                                       obj['IdentificadorTipoNorma']),

                    ]

                    full_resp.append(obj_resp)
            if not full_resp:
                raise  UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')

            return full_resp

    @property
    def faixa_nao_edificavel(self):
        # to do: maybe reduce the size of this funcion with a helper

        resp = self.api.consult_melhor_viario(self.setor, self.quadra)
        try:
            lista_melhor = resp['ArrayOfMelhoramentoViarioMelhoramentoViario']
        except KeyError:
            raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')

        if not lista_melhor:
            raise SQLNotFound(f'A quadra não foi encontrada: {self.setor}.{self.quadra}')
        elif type(lista_melhor) is not list:
            raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')
        # then there's a result that should be parsed
        else:
            full_resp = []
            for obj in lista_melhor:
                if obj['Resultado'] == 'NÃO' and obj['MelhoramentoFaixa'] == "FAIXA NÃO EDIFICÁVEL":
                    obj_resp = [
                        build_response('Incidência de faixa não edificável',
                                       'Indica se há incidência de faixa não edificável'
                                       'na quadra em que se situa o projeto',
                                       False)
                    ]
                    full_resp.append(obj_resp)
                elif obj['Resultado'] == 'SIM' and obj['MelhoramentoFaixa'] == "FAIXA NÃO EDIFICÁVEL":
                    obj_resp = [
                        build_response('Incidência de melhoramento viário',
                                       'Indica se há incidência de melhoramento viário ou faixa não edificável'
                                       'na quadra em que se situa o projeto',
                                       True),
                        build_response('Ano da norma',
                                       'Ano de publicação da norma que fundamenta o melhoramento viário',
                                       obj['AnoLeiMelhoramentoVigente']),
                        build_response('Tipo da norma',
                                       'Identifica o tipo da norma que fundamenta o melhoramento viário',
                                       obj['IdentificadorTipoNorma']),

                    ]

                    full_resp.append(obj_resp)
            if not full_resp:
                raise  UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')

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

    def ccm_ativo(self, cpf_ou_cnpj, numero):

        numero = str(numero)
        cpf_ou_cnpj = cpf_ou_cnpj.lower().strip()
        try:
            if cpf_ou_cnpj == 'cnpj':

                if len(numero) == 14:
                    resp = self.api.consult_ccm(cpf_ou_cnpj, numero)
                else:
                    raise ParametroInvalido(f'O número do {cpf_ou_cnpj} deve ser composto de 14 digitos numéricos')
            elif cpf_ou_cnpj == 'cpf':
                if len(numero) == 11:
                    resp = self.api.consult_ccm(cpf_ou_cnpj, numero)
                else:
                    raise ParametroInvalido(f'O número do {cpf_ou_cnpj} deve ser composto de 11 digitos numéricos')

            else:
                raise ParametroInvalido('Aceitamos apenas os parâmetros CPF ou CNPJ')

            if resp['Codigo'] == 0:
                for ccm in resp['DadosHistoricoCadastralTipo']['lstContribuinteMobiliario']\
                            ['DadosContribuinteMobiliarioTipo']:
                    status = ccm['codStatusCadastroContribuintesMobiliarios']
                    num_ccm = ccm['codCadastroContribuintesMobiliarios']
                    num_ccm = str(num_ccm)

                    while len(num_ccm) < 8:
                        num_ccm = '0' + num_ccm

                    valido = status == 1
                    if valido:
                        break

                return [build_response('CCM ativo?',
                                      'Identifica se o Cadastro de Contribuinte Imobiliário para o CNPJ ou CPF está ativo',
                                      valido),
                        build_response('Número CCM',
                                       'Número de Cadastro do Contribuinte Mobiliário',
                                       num_ccm)]

            elif resp['Codigo'] == 508:
                raise CPFouCNPJNotFound(f'O {cpf_ou_cnpj} de numero {numero} não foi encontrado')

            else:
                raise UnexpectedWebserviceResponse(f'Erro no consumo da webservice: {resp}')


        except (Fault, KeyError) as e:
            raise UnexpectedWebserviceResponse(f'Erro no consumo da webservice: {repr(e)}')

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
                niveis = detalhes_tombamento(tomb_resp['CodigoNivelPreservacao'])
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

                tomb.extend(niveis)

                tombamentos.append(tomb)

            return tombamentos

        else:
            raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')

    def logradouro_por_cep(self, cep):

        try:
            resp = self.api.consult_logradouro_por_cep(cep)
            if not resp:
                raise CEPNotFound(f'O Cep {cep} não foi encontrado')
            if resp['codRetorno'] == 0:
                #checa para ver se a lista de logradouros veio vazia
                if not resp['listaLogradouros']['Logradouro']:
                    raise CEPNotFound(f'O Cep {cep} não foi encontrado')

                dados = resp['listaLogradouros']['Logradouro'][0]

                tipo_logradouro = dados['nomTipoLogradouro'] or ''
                titulo_logradouro = dados['nomTituloLogradouro'] or ''
                preposicao_logradouro = dados['nomPreposicaoLogradouro'] or ''
                nom_logradouro = dados['nomLogradouro'] or ''

                logradouro_completo = ' '.join([tipo_logradouro,
                                                titulo_logradouro,
                                                preposicao_logradouro,
                                                nom_logradouro])

                return [
                    build_response(
                        'Nome do Logradouro',
                        'Identificação do logradouro',
                        logradouro_completo
                    ),
                    build_response('Bairro',
                                   'Identificação do bairro onde se situa o logradouro',
                                   dados['nomBairro']),
                    build_response('Código do logradouro',
                                   'Código identificador do logradoro na base de dados dos Correios',
                                   dados['codIdentificadorLogradouro'])
                ]
            else:
                raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')
        except Fault as e:
            raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {repr(e)}')

    @property
    def dados_lograouro_iptu(self):
        try:
            resp = self.api.consult_imovel_por_sql(self.setor, self.quadra, self.lote, self.digito)
            if resp['Codigo'] == 0:
                resp = serialize_object(resp, dict)
                try:
                    imovel = resp['imovel']
                    if imovel:
                        for key, value in imovel.items():
                            if value:

                                endereco = dados_endereco_iptu(imovel)
                                cep = str(endereco['cep'])
                                while len(cep) < 8:
                                    cep = '0' + cep
                                codlog = str(endereco['codlog'])
                                while len(codlog) < 6:
                                    codlog = '0' + codlog
                                return [
                                    build_response('Logradouro',
                                                   'Identificação do logradouro em que se situa o imóvel',
                                                   endereco['logradouro']
                                                   ),
                                    build_response('Numeração',
                                                   'Numeração de via do imóvel',
                                                   endereco['numeracao']),
                                    build_response('CEP',
                                                   'Código postal do imóvel',
                                                   cep),
                                    build_response('CodLog',
                                                   'Código oficial do Logradouro na base de dados da Prefeitura',
                                                   codlog),
                                    build_response('Bairro',
                                                   'Bairro em que se situa o imóvel',
                                                   endereco['bairro'])
                                ]


                        #significa que o imovel veio sem nenhum valor - acontece quando foi cancelado
                        else:
                            raise SQLNotFound(f'O Lote foi cancelado e/ou não possui dados cadastrados: {self.setor}.{self.quadra}.{self.lote}-{self.digito}')

                    else:
                        raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')
                except KeyError:
                    raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')
            elif resp['Codigo'] == 507:
                raise SQLNotFound(f'O Lote não foi encontrado: {self.setor}.{self.quadra}.{self.lote}-{self.digito}')

        except Fault as e:
            raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {repr(e)}')

    @property
    def param_constru_his(self):

        resp = self.api.obter_zoneamento(self.setor, self.quadra, self.lote)
        parametros_final = []
        try:
            if resp['Codigo'] == 4:
                raise SQLNotFound(f'O lota não foi encontrado: {self.setor}.{self.quadra}.{self.lote}')
            elif resp['Codigo'] == 0:
                zoneamento = resp['Zoneamentos']['Zoneamento']
                for zona in zoneamento:
                    cod = zona['CodigoZoneamento'][:2]
                    parametros = param_constru_his(cod)
                    if parametros:
                        parametros_final.append(parametros)
                if not parametros_final:
                    raise ZonaUsoNotFound(f'As zonas de uso encontradas nao possuem parametros para HIS: {zoneamento}')
                else:
                    return parametros_final

        except KeyError as e:
            raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp} {repr(e)}')

    @property
    def tx_permeab_his(self):

        resp = self.api.obter_zoneamento(self.setor, self.quadra, self.lote)
        try:
            if resp['Codigo'] == 4:
                raise SQLNotFound(f'O lota não foi encontrado: {self.setor}.{self.quadra}.{self.lote}')
            elif resp['Codigo'] == 0:
                zoneamento = resp['Zoneamentos']['Zoneamento']
                resp_final = []
                for zona in zoneamento:
                    tx = tx_permeab_his(zona)
                    if tx:
                        resp_final.append(tx)
                if not resp_final:
                    raise ZonaUsoNotFound(f'As zonas de uso encontradas nao possuem parametros para HIS: {zoneamento}')
                return resp_final
            else:
                raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')

        except KeyError as e:
            raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp} {repr(e)}')

    @property
    def zona_uso_permite_his_declaratorio(self):

        resp = self.api.obter_zoneamento(self.setor, self.quadra, self.lote)
        try:
            if resp['Codigo'] == 4:
                raise SQLNotFound(f'O lota não foi encontrado: {self.setor}.{self.quadra}.{self.lote}')
            elif resp['Codigo'] == 0:
                resp_final = []
                zoneamento = resp['Zoneamentos']['Zoneamento']
                for zona in zoneamento:
                    cod = zona['CodigoZoneamento'][:2]
                    try:
                        permite = zona_uso_permite_declaratorio(cod)
                        resp_final.append(permite)
                    except IndexError:
                        pass
                #se nao encontrou nenhuma zona de uso, levanta erro
                if not resp_final:
                    return ZonaUsoNotFound(f'As zonas de uso encontradas nao possuem parametros para HIS: {zoneamento}')
                #checa se tem mais de uma zona de uso
                elif len(resp_final) > 1:
                    return build_response(
                            'Zona de uso permite declaratório?',
                            'Identifica se a zona de uso permite HIS declaratório',
                            False)
                #retorna a resposta
                return build_response(
                            'Zona de uso permite declaratório?',
                            'Identifica se a zona de uso permite HIS declaratório',
                            resp_final[0])
            else:
                raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')

        except KeyError:
            raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: Chave não encontrada {resp}')

    def zona_uso_aceita_his_ou_hmp(self, tipologia_empreendimento):

        resp = self.api.obter_zoneamento(self.setor, self.quadra, self.lote)
        try:
            if resp['Codigo'] == 4:
                raise SQLNotFound(f'O lota não foi encontrado: {self.setor}.{self.quadra}.{self.lote}')
            elif resp['Codigo'] == 0: #zona de uso é sempre o primeiro item
                zoneamento = resp['Zoneamentos']['Zoneamento']
                zona_uso = zoneamento[0]
                cod = zona_uso['CodigoZoneamento'][:2]
                check = checar_tipologia_empreendimento(cod, tipologia_empreendimento)
                return build_response(
                    f'Aceita {tipologia_empreendimento}',
                    f'Empreendimento de tipo {tipologia_empreendimento} é permitido na zona de uso do imóvel?',
                    check)

        except KeyError as e:
            raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp} {repr(e)}')


    @property
    def zoneamento(self):

        resp = self.api.obter_zoneamento(self.setor, self.quadra, self.lote)
        try:
            if resp['Codigo'] == 4:
                raise SQLNotFound(f'O lota não foi encontrado: {self.setor}.{self.quadra}.{self.lote}')
            elif resp['Codigo'] == 0:

                zonas = resp['Zoneamentos']['Zoneamento']
                zoneamento_formatado = []
                for zona in zonas:
                    parsed = pegar_dados_zoneamento(zona)
                    legislacao = f"{zona['CodigoTipoLegislacao']}{zona['NumeroLegislacao']} de {zona['AnoLegislacao']}"
                    response = [build_response('Sigla',
                                               'Sigla da Zona',
                                               parsed['sigla']),
                                build_response('Descrição',
                                               'Descrição da zona',
                                               parsed['descricao']),
                                build_response('Tipo de Zoneamento',
                                               'Identifica o tipo de zoneamento do imóvel',
                                               parsed['tipo_zoneamento']),
                                build_response('Legislação',
                                               "Legislação que cria/regulamenta a zona",
                                               legislacao)]
                    if parsed.get('perimetro_ambiental'):
                        response.append(build_response('Perímetro Ambiental',
                                                       'Identificação do Perímetro Ambiental em que se situa o imóvel',
                                                       parsed['perimetro_ambiental']))
                    zoneamento_formatado.append(response)

                return zoneamento_formatado

            else:
                raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')
        except KeyError as e:
            raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp} {repr(e)}')

    @property
    def subprefeitura(self):

        resp = self.api.obter_zoneamento(self.setor, self.quadra, self.lote)
        try:
            if resp['Codigo'] == 4:
                raise SQLNotFound(f'O lota não foi encontrado: {self.setor}.{self.quadra}.{self.lote}')
            elif resp['Codigo'] == 0:
                zona = resp['Zoneamentos']['Zoneamento'][0]
                try:
                    subs = pegar_subprefeitura(zona)
                    return [build_response('Subprefeitura',
                                           'Identificação da subprefeitura em que se situa o imóvel',
                                           subs['descricao']),
                            build_response('Sigla',
                                           'Sigla da subprefeitura em que se situa o imóvel',
                                           subs['sigla'])
                            ]
                except IndexError:
                    raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')
            else:
                raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp}')
        except KeyError as e:
            raise UnexpectedWebserviceResponse(f'Erro no formato da resposta: {resp} {repr(e)}')
















