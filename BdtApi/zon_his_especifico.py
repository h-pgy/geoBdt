import pandas as pd
from .helpers import build_response

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


def tx_permeab_his(zona):

    cota_ambiental =  _pegar_cota_ambiental(zona)

    if cota_ambiental:
        pa = cota_ambiental['Perímetro de Qualificação Ambiental']
        taxas = pd.read_excel('data/dados_zoneamento_his.xlsx', sheet_name='taxa_permeab_min')
        labels = taxas.iloc[0]
        dados = taxas.drop(0)
        resp = dados[dados['perim_amb'] == pa].to_dict(orient='records')[0]

        final = []
        for key, value in resp.items():
            final.append(build_response(key, labels[key], value))
        return final
    return []


def param_constru_his(cod_zona_uso):

    cod_zona_uso = int(cod_zona_uso)
    try:
        param_constru_his = pd.read_excel('data/dados_zoneamento_his.xlsx', sheet_name='padrao_ocup_HIS', encoding = 'utf-8')
        labels = param_constru_his.iloc[0]
        dados = param_constru_his.drop(0)
        resp = dados[dados['cod_siszon'] == cod_zona_uso].to_dict(orient='records')[0]

        final = []
        for key, value in resp.items():
            if pd.isna(value):
                value = None
            final.append(build_response(key, labels[key], value))

        return final
    except IndexError:
        return []