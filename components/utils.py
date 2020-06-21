import plotly.express as px
import pandas as pd
from datetime import datetime as dt


def get_df(path='data/predictions.csv'):
    df = pd.read_csv(path)
    df['data'] = pd.to_datetime(df['data'], format="%d/%m/%Y")
    return df

def get_anomaly_color(value):
    color_index = 0
    anomaly = 0
    while anomaly < value and color_index < 8:
        anomaly += 1.11
        color_index += 1

    return px.colors.sequential.YlOrRd[color_index]

def get_formated_price(value):
    value = '%.2f' % value
    preco = list(str(value)[::-1])[3:]
    decimal = list(str(value)[::-1])[:2]
    decimal.reverse()
    added = 0
    for i in range(1, len(preco)):
        if i % 3 == 0:
            preco.insert(i+added, '.')
            added += 1
    preco.reverse()
    return 'R$%s,%s ' % (''.join(preco), ''.join(decimal))

def get_formated_date(value):
    if value != 'NaT':
        date = dt.strptime(value, '%Y-%m-%d')
        return str(date.strftime('%d/%m/%Y'))
    return 'Sem data definida'

def get_renamed_df(df):
    return df.rename(
        columns={
            'data': 'Data',
            'estado': 'UF',
            'nome': 'Compra',
            'preco': 'Preço/Unidade',
            'valor_total': 'Valor Total',
            'quantidade': 'Qtd.',
            'anomalo': 'Suspeitômetro',
            'valor_total': 'Preço Total'
        }
    )
