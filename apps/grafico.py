import json
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from datetime import datetime as dt
from datetime import date
from app import app
from dash.dependencies import Input, Output

with open('data/geojson_uf.json') as response:
    geojson_uf = json.load(response)

colors = {
    'background': '#343a40',
    'text': 'white'
}

df = pd.read_csv('data/predictions.csv')
df['data'] = pd.to_datetime(df['data'])
current_year = 2020

map_df = pd.read_csv('data/predictions.csv')
map_df = map_df[map_df['anomalo'] != 1]
map_df = map_df[['estado', 'anomalo']].groupby('estado', as_index=False).mean()

fig = px.choropleth(map_df,
    geojson=geojson_uf,
    locations='estado',
    color='anomalo',
    featureidkey='properties.UF_05',
    scope='south america',
    color_continuous_scale='ylorrd_r'
)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0,
                          "b": 0}, clickmode='event+select')

def update_dataframe(df, start_date, end_date, price_limit, amount_limit, states_clicked):
    if states_clicked is not None:
        states = [point['location'] for point in states_clicked['points']]
        updated_df = df[df['estado'].isin(states)]
    else:
        updated_df = df

    start_date = dt.strptime(start_date, '%Y-%m-%d')
    end_date = dt.strptime(end_date, '%Y-%m-%d')
    updated_df = updated_df[
        (
            (updated_df['data'] >= start_date)
            & (updated_df['data'] <= end_date)
        ) | (updated_df['data'].isnull())
    ]

    updated_df = updated_df[
        (updated_df['preco'] >= price_limit[0])
        & (updated_df['preco'] <= price_limit[1])
    ]

    updated_df = updated_df[
        (updated_df['quantidade'] >= amount_limit[0])
        & (updated_df['quantidade'] <= amount_limit[1])
    ]

    updated_df = updated_df.rename(columns={
        'data': 'Data',
        'estado': 'UF',
        'nome': 'Compra',
        'preco': 'Preço/Unidade',
        'quantidade': 'Unidades'
    })

    updated_df = updated_df.assign(
        **updated_df.select_dtypes(['datetime']).astype(str).to_dict('list')
    )
    return updated_df

def create_row(row):
    tr_children = []
    for index, value in row.iteritems():
        if index not in ['anomalo', 'Fonte']:
            if index == 'Compra':
                style = {'fontSize': 'small', 'textAlign': 'center'}
                td_children = [value, ' (', html.A('Fonte', href=row['Fonte']), ')']
            else:
                style = {'fontSize': 'small', 'textAlign': 'center'}
                td_children = [value]
            tr_children.append(html.Td(style=style, children=td_children))

    if row['anomalo'] < 5:
        return html.Tr(className='suspeito', children=tr_children)
    return html.Tr(children=tr_children)

def update_table(df):
    return html.Table(
        className='table table-sm table-hover',
        style={'backgroundColor': 'white'},
        children=[
            html.Thead(
                html.Tr(
                    [
                        html.Th(column, style={'fontSize': 'small', 'textAlign': 'center'})
                        for column in df.columns if column not in ['anomalo', 'Fonte']
                    ]
                )
            ),
            html.Tbody(
                [create_row(row) for index, row in df.iterrows()]
            ),
        ]
    )

layout = html.Div(
    children=[
        html.H1(
            id='dados-estado',
            children='Dados de Compras de Respiradores',
            style={'textAlign': 'center',
                    'color': colors['text']}
        ),

        html.Div(
            className='row row-cols-1 row-cols-md-3 mt-1',
            children=[
                html.Div(
                    className='col text-center',
                    children=[
                        dcc.DatePickerRange(
                            id='date-picker',
                            display_format='D/M/Y',
                            min_date_allowed=df['data'].min(),
                            max_date_allowed=df['data'].max(),
                            initial_visible_month=dt(
                                current_year, df['data'].max().month, 1),
                            start_date=df['data'].min(),
                            end_date=df['data'].max(),
                        ),
                    ],
                ),
                html.Div(
                    className='col text-center',
                    children=[
                        html.Span(
                            'Faixa de Preço: R$ %s - R$ %s' % (
                                df['preco'].min(), df['preco'].max()),
                            id='display-price-slider',
                            className="price-span",
                            style={'color' : colors['text']}
                        ),
                        dcc.RangeSlider(
                            id='price-slider',
                            min=df['preco'].min(),
                            max=df['preco'].max(),
                            step=1,
                            value=[df['preco'].min(), df['preco'].max()],
                        )
                    ]
                ),
                html.Div(
                    className='col text-center',
                    children=[
                        html.Span(
                            'Quantidade: %s - %s' % (df['quantidade'].min(),
                                                    df['quantidade'].max()),
                            id='display-amount-slider',
                            style={'color' : colors['text']}
                        ),
                        dcc.RangeSlider(
                            id='amount-slider',
                            min=df['quantidade'].min(),
                            max=df['quantidade'].max(),
                            step=1,
                            value=[df['quantidade'].min(
                            ), df['quantidade'].max()],
                        )
                    ]
                ),
            ]
        ),

        html.Div(
            className='row',
            children=[
                html.Div(
                    className='col-12 p-0',
                    children=dcc.Graph(
                        id="choropleth",
                        figure=fig,
                    ),
                    style={'maxWidth': '30%'}
                ),
                html.Div(
                    className='col-12 p-0',
                    children=html.Div(
                        id='data-table',
                        className='table-responsive',
                    ),
                    style={'maxWidth': '70%', 'maxHeight': '450px', 'overflow': 'auto'},
                ),
            ]
        ),

    ]
)

@app.callback(
    Output('data-table', 'children'),
    [
        Input('date-picker', 'start_date'),
        Input('date-picker', 'end_date'),
        Input('price-slider', 'value'),
        Input('amount-slider', 'value'),
        Input('choropleth', 'selectedData')
    ],
)
def update_data(start_date, end_date, price_limit, amount_limit, state_clicked):
    updated_df = update_dataframe(df, start_date[:10], end_date[:10], price_limit, amount_limit, state_clicked)
    return update_table(updated_df)


@app.callback(
    Output('display-price-slider', 'children'),
    [Input('price-slider', 'value')]
)
def update_price_slider(limits):
    return 'Faixa de Preço: R$%s - R$%s' % (limits[0], limits[1])


@app.callback(
    Output('display-amount-slider', 'children'),
    [Input('amount-slider', 'value')]
)
def update_amount_slider(limits):
    return 'Quantidade: %s - %s' % (limits[0], limits[1])

# for data in df['data']:
#     print(pd.isnull(data))
