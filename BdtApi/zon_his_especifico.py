import pandas as pd
from .helpers import build_response

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