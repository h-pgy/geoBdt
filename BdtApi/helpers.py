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
    tipo_logradouro = imovel['codTipoLogradouroField']['valueField'] or ''
    tipo_logradouro = tipo_logradouro.strip()
    titulo_logradouro = imovel['txtTituloLogradouroField']['valueField'] or ''
    titulo_logradouro= titulo_logradouro.strip()
    preposicao_log = imovel['txtPreposicaoLogradouroField']['valueField'] or ''
    nom_logradouro = imovel['nomLogradouroField']['valueField'] or ''
    nom_logradouro = nom_logradouro.strip()
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

def pegar_dados_zoneamento(zona):
    cod_zona = int(zona['CodigoZoneamento'][:2])
    df = pd.read_excel('data/codigos_zoneamento_SMDU.xlsx', sheet_name='codigos_zoneamento')
    dados_zon = df[df['codigo'] == cod_zona].to_dict(orient='records')[0]
    tipo = dados_zon['tipo_zoneamento']
    if tipo == 'Zona de Uso':
        return dados_zon
    elif tipo == 'Macroarea e Setores da MEM':
        perimetro = int(zona['CodigoZoneamento'][-6:-2])
        df = pd.read_excel('data/codigos_zoneamento_SMDU.xlsx', sheet_name='codigos_macroarea_e_mem')
        dados_macroarea = df[df['codigo_perimetro'] == perimetro].to_dict(orient='records')[0]
        dados_zon.update(dados_macroarea)
        return dados_zon
    elif tipo == 'Quota Ambiental':
        perimetro = int(zona['CodigoZoneamento'][-6:-2])
        dados_zon['perimetro_ambiental'] = f'PA-{perimetro}'
        return dados_zon


def pegar_subprefeitura(zona):
    cod_subprefeitura = int(zona['CodigoZoneamento'][-2:])
    df = pd.read_excel('data/codigos_zoneamento_SMDU.xlsx', sheet_name='codigos_subprefeituras')

    return df[df['codigo'] == cod_subprefeitura].to_dict(orient='records')[0]