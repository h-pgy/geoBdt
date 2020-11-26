import pandas as pd

def build_response(label, description, value):
    """Simple function for making code leaner"""

    return {'label' : label,
            'description' : description,
            'value' : value}

#HELPERES CIT

def detalhes_tombamento(nivel):
    try:
        niveis_cit = pd.read_excel('data/niveis_tombamento_cit.xlsx')
        labels = niveis_cit.iloc[0]
        dados = niveis_cit.drop(0)
        resp = dados[dados['nivel_tombamento']==nivel].to_dict(orient = 'records')[0]

        final = []
        for key, value in resp.items():
            if value == 'SIM':
                value = True
            final.append(build_response(key, labels[key], value))

        return final
    except IndexError:
        return []

#HELPERS PARA DADOS IPTU/TPCL

def pegar_rua_iptu(imovel):
    tipo_logradouro = imovel['codTipoLogradouroField']['valueField'].strip()
    titulo_logradouro = imovel['txtTituloLogradouroField']['valueField'].strip()
    preposicao_log = imovel['txtPreposicaoLogradouroField']['valueField'] or ''
    nom_logradouro = imovel['nomLogradouroField']['valueField'].strip()
    rua_completo = ' '.join([tipo_logradouro,
                             titulo_logradouro,
                             preposicao_log,
                             nom_logradouro])

    return rua_completo


def dados_endereco_iptu(imovel):

    return {
        'logradouro' : pegar_rua_iptu(imovel),
        'numeracao' : imovel['numImovelField'],
        'cep' : imovel['numCEPField'],
        'codlog' : imovel['numCodLogField']['valueField'],
        'bairro' : imovel['nomBairroImovelField']['valueField']
    }



# HELPERS PARA O ZONEAMENTO

def parsear_zoneamento(resp):
    """Parses zoning API resposne data to a more
    semantic response"""

    if resp['Codigo'] == 0:
        zoneamento_imovel = []
        zoneamento = resp['Zoneamentos']['Zoneamento']
        for zona in zoneamento:
            dados_zona = _pegar_setor_mem(zona) \
                         or _pegar_cota_ambiental(zona) \
                         or _pegar_perim_incentivo(zona) \
                         or _pegar_zona_de_uso(zona)

            zoneamento_imovel.append(dados_zona)

        return zoneamento_imovel
    else:
        return None

def _pegar_zona_de_uso(dici_resp):

    descr_zona_uso = dici_resp['DescricaoZonaUso'].strip()
    sigla = dici_resp['SiglaZonaUso'].strip()
    tipo_lei = dici_resp['CodigoTipoLegislacao'].strip()
    numero_lei = dici_resp['NumeroLegislacao']
    ano_lei = dici_resp['AnoLegislacao']
    legislacao = f'{tipo_lei} {numero_lei} de {ano_lei}'

    return {
        'SiglaZonaUso': sigla,
        'DescricaoZonaUso': descr_zona_uso,
        'Legislacao': legislacao,
        'TipoZoneamento': 'Zona de Uso'
    }


def _pegar_perim_incentivo(dici_resp):

    if dici_resp['DescricaoZonaUso'].strip() == 'PERIMETRO DE INCENTIVO AO DESENVOLVIMENTO ECONOMICO':
        cod_perimetro = int(dici_resp['CodigoZoneamento'][-4:-2])

        return {
            'TipoZoneamento': 'Perímetro de Incentivo ao Desenvolvimento Econômico',
            'CodigoPerimetro': cod_perimetro
        }
    else:
        return None


def _pegar_cota_ambiental(dici_resp):
    if dici_resp['DescricaoZonaUso'].strip() == 'QUOTA AMBIENTAL':

        cod_setor = int(dici_resp['CodigoZoneamento'][-4:-2])
        perimetro = f'PA {cod_setor}'

        return {
            'TipoZoneamento': 'Quota Ambiental',
            'Perímetro de Qualificação Ambiental': perimetro
        }
    else:
        return None


def _pegar_setor_mem(dici_resp):
    de_para_setores_da_mem = {
        18: 'Centro',
        15: 'Avenida Cupecê',
        12: 'Faria Lima- Água Espraida- Chucri Zaidan',
        17: 'Fernão Dias',
        14: 'Arco Jacú Pêssego',
        13: 'Arco Jurubatuba',
        8: 'Arco Leste',
        16: 'Noroeste',
        11: 'Arco Pinheiros',
        10: 'Arco Tamanduateí',
        9: 'Arco Tietê'
    }

    if dici_resp['DescricaoZonaUso'].strip() == 'MACROAREA E SETORES DA MEM':

        cod_setor = dici_resp['CodigoZoneamento'][-4:-2]
        try:
            nome_do_setor = de_para_setores_da_mem[int(cod_setor)]
        except KeyError:
            nome_do_setor = None

        return {'CodigoSetor': cod_setor,
                'NomeSetor': nome_do_setor,
                'TipoZoneamento': 'Setores da Macroárea de Estruturação Metropolitana'}
    else:
        return None

