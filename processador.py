#!/usr/bin/env python3
# coding: utf-8

import json
from collections import OrderedDict
from datetime import datetime as dt
import pandas as pd
from sinonimos import generalizar

num_textos = OrderedDict()
textos_num = {}


def subs_texto(t):
    index = textos_num.get(t)
    if not index:
        index = len(textos_num)
        textos_num[t] = index
        num_textos[index] = t
    return index


def processar_registro(r):
    return [
        *[subs_texto(r[s]) for s in ['Fornecedor', 'Serviços', 'Mês']],
        r['Valor Bruto']
    ]


def abrir_planilha():
    try:
        df = pd.read_hdf('planilha.hdf', 'dados')
    except:
        df = pd.read_excel('Planilha_Exportacao.xlsx')
        df.to_hdf('planilha.hdf', 'dados', mode='w')

    # converter string-floats para floats
    for col in ['Valor Bruto', 'Tributos', 'Valor Liquido']:
        df[col] = df[col].apply(lambda x: float(x.replace(',', '.')))

    # generalizar nomes
    col = 'Fornecedor'
    df[col] = df[col].apply(generalizar)

    # mês em formato mais facilmente ordenável
    col = 'Mês'
    df[col] = df[col].apply(lambda x: x[3:] + '/' + x[:2])
    df['Ano'] = df['Mês'].apply(lambda x: x[:4])

    # ignorar algumas colunas por enquanto
    for col in ['Contrato', 'Agência Contratante', 'Tributos',
                'Valor Liquido']:
        df.drop(col, axis=1, inplace=True)

    return df


def total_por_mes(df):
    somas = df.groupby('Mês', as_index=False).sum()
    col = 'Valor Bruto'
    somas[col] = somas['Valor Bruto'].apply(round)
    return somas.to_dict(orient='split')['data']


def total_por_ano(df):
    somas = df.groupby('Ano', as_index=False).sum()
    col = 'Valor Bruto'
    somas[col] = somas['Valor Bruto'].apply(round)
    return somas.to_dict(orient='split')['data']


def total_por_fornecedor(df):
    '''Retorna o total acumulado por cada fornecedor.'''
    return df.groupby('Fornecedor', as_index=False).sum().sort_values(
        'Valor Bruto', ascending=False)


def maiores_fornecedores(df, n=20):
    '''Retorna o total acumulada pelos n maiores fornecedores.'''
    return total_por_fornecedor(df).head(n).Fornecedor.tolist()


def total_por_fornecedor_por_data(df, data):
    return df.groupby([data, 'Fornecedor'], as_index=False).sum().sort_values(
        [data, 'Valor Bruto'])


def total_por_maiores_fornecedores_no_periodo_por_data(df, data, n=20):
    return total_por_fornecedor_por_data(df, data).groupby(data).tail(n)


def total_por_maiores_fornecedores_globais_por_data(df, data, n=20):
    df = total_por_fornecedor_por_data(df, data)
    return df[df['Fornecedor'].isin(maiores_fornecedores(df, n))]


def listar_datas(df, data):
    return df[data].drop_duplicates().tolist()


def int_data(texto, tipo):
    return (int(dt.strptime(texto, '%Y' if tipo is 'Ano' else '%Y/%m')
            .timestamp())*1000)


def analises_por_data(df, data, n=20, fracoes=[.5, .1, .01]):
    '''
    Retorna algumas análises nos dados.
    n: n maiores linhas que se deseja comparar
    fracao: fração das maiores linhas que se deseja comparar
    '''
    df = total_por_fornecedor_por_data(df, data)
    agrup = df.groupby(data)

    # n por data
    contagens = agrup.size()

    totais_data = agrup.sum()
    porcentual_n_maiores = agrup.tail(n).groupby(data).sum()/totais_data * 100

    # porcentagem do topo que se deseja contabilizar
    def porcentual_frac_maiores(fracao):
        return (pd.concat([
            y.tail(int(len(y)*fracao)) for y in
            [agrup.get_group(x) for x in agrup.groups]
        ]).groupby(data).sum() / totais_data * 100)['Valor Bruto']

    def formatar(valores):
        return list(zip(datas, valores.tolist()))

    datas = [int_data(x, tipo=data) for x in listar_datas(df, data)]

    return [{
        'name': 'Quantidade de fornecedores',
        'type': 'column',
        'data': formatar(contagens),
        'yAxis': 1,
    }, {
        'name': 'Total pago',
        'type': 'column',
        'data': formatar(totais_data['Valor Bruto']),
        'yAxis': 2,
        'tooltip': {
            'valuePrefix': 'R$ ',
        }
    }, *[{
        'name': 'Porcentagem acumulada por %s%% maiores' % int(f*100),
        'data': formatar(porcentual_frac_maiores(f)),
        'tooltip': {
            'valueSuffix': '%',
        }
    } for f in fracoes], {
        'name': 'Porcentagem acumulada por %s maiores' % n,
        'data': formatar(porcentual_n_maiores['Valor Bruto']),
        'tooltip': {
            'valueSuffix': '%',
        }
    }]


def serializar_categorias(df, data):
    return [{
        'name': i,
        'data': [(int_data(m, data), v)
                 for m, v in zip(d[data], d['Valor Bruto'])]
    } for i, d in df.groupby('Fornecedor').aggregate(
        lambda x: x.tolist()
    ).to_dict('index').items()]

# saida = {
#     'totalMes': analises_por_data(df, 'Ano'),
#     # 'totalMes': serializar_categorias(
#     #     total_por_maiores_fornecedores_globais_por_data(df, 'Mês')),
#     # 'totalAno': total_por_ano(df)
#     # 'totalMes': total_por_mes(df)
# }

# arq = open('dados.json', 'w')
# json.dump(saida, arq)
# arq.close()
