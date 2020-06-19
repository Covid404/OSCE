import json
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from datetime import datetime as dt
from datetime import date
import pandas as pd
import dash_table
from app import app
from apps import grafico, quem_somos

df = pd.read_csv('data/predictions.csv')
df['data'] = pd.to_datetime(df['data'])
current_year = 2020

df = df.sort_values('preco', ascending=False)[:5]

with open('data/geojson_uf.json') as response:
    geojson_uf = json.load(response)

map_df = pd.read_csv('data/predictions.csv')
map_df = map_df[map_df['anomalo'] != 1]
map_df = map_df.sort_values('anomalo', ascending=False)[:5]
map_df = map_df[['estado', 'anomalo']].groupby('estado', as_index=False).mean()
map_df = map_df.rename(columns={'anomalo': 'media de anomalia'})
map_df = map_df.sort_values('media de anomalia', ascending=False)[:5]

fig = px.choropleth(map_df,
                    geojson=geojson_uf,
                    locations='estado',
                    color='media de anomalia',
                    featureidkey='properties.UF_05',
                    scope='south america',
                    color_continuous_scale='ylorrd'
                    )

fig.update_layout(margin={"r": 0, "t": 0, "l": 0,
                          "b": 0}, clickmode='event+select')

colors = {
    'background': '#343a40',
    'text': 'white'
}

layout = html.Div(
    style={'textAlign': 'center'},
    className="table-parent",
    children=[
        html.Div(
            className='presentation-text-container',
            children=[
                html.H2(
                    'COVIS - Sistema de rastreamento de fraude',
                    style={
                        'color': 'rgba(255,255,255,0.9)',
                        'marginBottom': '2%'
                    }
                ),
                html.Span(
                    'Bla bla bla bla - textinho do ASIAN CEO',
                    style={
                        'color': 'rgba(255,255,255,0.9)',
                        'fontSize': '20px',
                        'fontWeight': '500'
                    }
                )
            ],
            style={
                'marginBottom': '2%'
            }
        ),

        html.H3(
            'Top 5 Fraudes',
            style={
                'color': '#ff7070',
                'marginBottom': '2%'
            }
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
                            style={'color': colors['text']}
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
                            style={'color': colors['text']}
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
            className='d-flex justify-content-center',
            children=[
                html.Div(
                    className='row',
                    style={
                        'width' : '95%',
                    },
                    children=[
                        html.Div(
                            className='col-12 p-0',
                            children=dcc.Graph(
                                id="choropleth",
                                figure=fig,
                            ),
                            style={
                                'maxWidth': '30%',
                            }
                        ),
                        html.Div(
                            className='col-12 p-0',
                            children=html.Div(
                                id='data-table',
                                className='table-responsive table-striped',
                            ),
                            style={
                                'maxWidth': '70%',
                                'maxHeight': '450px',
                                'overflow': 'auto'
                            },
                        ),
                    ]
                ),
            ]
        ),

        html.P(
            'Caso você deseje conferir a tabela por completo, basta clicar no botão abaixo.',
            style={
                'color': 'rgba(255,255,255,0.9)',
                'marginTop': '2%'
            }
        ),

        html.A(
            'Redirecionar',
            id='redirect',
            className='btn btn-primary',
            href='/data'
        )
    ]
)
