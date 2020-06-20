import plotly.express as px
import pandas as pd
from datetime import datetime as dt


def get_df(path='data/predictions.csv'):
    df = pd.read_csv(path)
    df['data'] = pd.to_datetime(df['data'])
    return df

anomaly_colors = []
for color in px.colors.sequential.YlOrRd:
    anomaly_colors += [
        color.replace(')', ',{})'.format(0.25)),
        color.replace(')', ',{})'.format(0.50)),
        color.replace(')', ',{})'.format(0.75)),
        color.replace(')', ',{})'.format(1))
    ]

def get_anomaly_color(value):
    color_index = 0
    anomaly = 0
    while anomaly < value and color_index < 35:
        anomaly += 0.277
        color_index += 1

    return anomaly_colors[color_index]


def get_formated_price(value):
    value = '%.2f' % value
    preco = list(str(value)[::-1])[3:]
    decimal = list(str(value)[::-1])[:2]
    decimal.reverse()
    for i in range(len(preco) - 1):
        if i != 0 and i % 3 == 0:
            preco.insert(i, '.')
    preco.reverse()
    return 'R$ %s,%s ' % (''.join(preco), ''.join(decimal))

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
            'quantidade': 'Unidades',
            'anomalo': 'Suspeitômetro'
        }
    )