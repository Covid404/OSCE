import json
import urllib
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from datetime import datetime as dt
from datetime import date
from app import app
from dash.dependencies import Input, Output
from components import utils, table
import components.utils as utils

with open('data/geojson_uf.json') as response:
    geojson_uf = json.load(response)

colors = {
    'background': '#343a40',
    'text': 'rgba(255,255,255,0.9)'
}

df = utils.get_df()
current_year = 2020

map_df = pd.read_csv('data/predictions.csv')
map_df = map_df[map_df['anomalo'] != 1]
map_df = map_df[['estado', 'anomalo']].groupby('estado', as_index=False).mean()
map_df = map_df.rename(columns={'anomalo': 'Suspeitômetro', 'estado': 'UF'})

fig = px.choropleth(map_df,
    geojson=geojson_uf,
    locations='UF',
    color='Suspeitômetro',
    featureidkey='properties.UF_05',
    scope='south america',
    color_continuous_scale='ylorrd',
    range_color=[0, 10],
)

fig.update_layout(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    clickmode='event+select',
    height=550
)


def update_dataframe(df, start_date, end_date, price_limit, amount_limit, states_clicked, alert):
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

    if alert != []:
        updated_df = updated_df[updated_df['anomalo_label'].isin(alert)]

    updated_df = utils.get_renamed_df(updated_df)

    updated_df = updated_df.assign(
        **updated_df.select_dtypes(['datetime']).astype(str).to_dict('list')
    )
    return updated_df

do_not_create = ['Fonte', 'anomalo_label', 'nome_original', 'id']

layout = html.Div(
    children=[
        html.H3(
            id='dados-estado',
            children='Compras de Ventiladores',
            style={
                'textAlign': 'center',
                'color': colors['text'],
                'marginTop': '1%'
            }
        ),

        html.Div(
            className='row row-cols-1 row-cols-md-4 mt-5',
            children=[
                html.Div(
                    className='col pr-0 pl-0 text-center',
                    style={'fontSize': 'small'},
                    children=[
                        dcc.DatePickerRange(
                            id='date-picker',
                            display_format='D/M/Y',
                            min_date_allowed=df['data'].min(),
                            max_date_allowed=df['data'].max(),
                            initial_visible_month=dt(current_year, df['data'].max().month, 1),
                            start_date=df['data'].min(),
                            end_date=df['data'].max(),
                        ),
                    ],
                ),
                html.Div(
                    className='col pr-0 pl-0 text-center',
                    style={'fontSize': 'small'},
                    children=[
                        html.Div(
                            html.Span(id='display-price-slider'),
                            style={
                                'color': colors['text'],
                                'marginBottom': '1%',
                            }
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
                    className='col pr-0 pl-0 text-center',
                    style={'fontSize': 'small'},
                    children=[
                        html.Div(
                            html.Span(
                                id='display-amount-slider',
                            ),
                            style={
                                'color': colors['text'],
                                'marginBottom': '1%',
                            }
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
                html.Div(
                    className='col pr-0. pl-0 text-center',
                    style={'fontSize': 'small'},
                    children=[
                        dcc.Dropdown(
                            id='alert-picker',
                            options=[
                                {'label': 'Baixo', 'value': 'baixo'},
                                {'label': 'Médio', 'value': 'medio'},
                                {'label': 'Alto', 'value': 'alto'},
                            ],
                            placeholder='Nível de Alerta do Suspeitômetro',
                            searchable=False,
                            multi=True,
                            value=[]
                        )
                    ]
                )
            ]
        ),

        html.Div(
            style={'textAlign': 'right', 'fontSize': 'small', 'color': colors['text']},
            children=[
                'Baixe essa tabela ',
                html.A(
                    children='AQUI',
                    id='download-csv',
                    download='osce-dados.csv',
                    href='',
                    target='_blank'
                )
            ]
        ),

        html.Div(
            className='row',
            children=[
                html.Div(
                    className='col p-0',
                    children=dcc.Graph(
                        id="choropleth",
                        figure=fig,
                    ),
                    style={'maxWidth': '30%'}
                ),
                html.Div(
                    className='col p-0',
                    children=html.Div(
                        id='data-table',
                        style={'backgroundColor': '#f8f9fa'},
                        className='table-responsive',
                    ),
                    style={
                        'maxWidth': '70%',
                        'maxHeight': '550px',
                        'overflow': 'auto',
                    },
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
        Input('choropleth', 'selectedData'),
        Input('alert-picker', 'value')
    ],
)
def update_data(start_date, end_date, price_limit, amount_limit, state_clicked, alert):
    print(alert)
    updated_df = update_dataframe(
        df,
        start_date[:10],
        end_date[:10],
        price_limit,
        amount_limit,
        state_clicked,
        alert
    )
    return table.create_table(updated_df, do_not_create)


@app.callback(
    Output('display-price-slider', 'children'),
    [Input('price-slider', 'value')]
)
def update_price_slider(limits):
    return 'Preço/Unidade: %s - %s' % (
        utils.get_formated_price(limits[0]),
        utils.get_formated_price(limits[1])
    )

@app.callback(
    Output('display-amount-slider', 'children'),
    [Input('amount-slider', 'value')]
)
def update_amount_slider(limits):
    return 'Quantidade: %s - %s' % (limits[0], limits[1])

@app.callback(
    Output('download-csv', 'href'),
    [
        Input('date-picker', 'start_date'),
        Input('date-picker', 'end_date'),
        Input('price-slider', 'value'),
        Input('amount-slider', 'value'),
        Input('choropleth', 'selectedData'),
        Input('alert-picker', 'value')
    ]
)
def update_csv_download(start_date, end_date, price_limit, amount_limit, state_clicked, alert):
    updated_df = update_dataframe(
        df,
        start_date[:10],
        end_date[:10],
        price_limit,
        amount_limit,
        state_clicked,
        alert
    )
    csv = updated_df.to_csv(index=False,encoding='utf-8')    
    csv = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv)
    return csv