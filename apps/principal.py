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
map_df = map_df[['estado', 'anomalo']].groupby('estado', as_index=False).count()

fig = px.choropleth(map_df,
                    geojson=geojson_uf,
                    locations='estado',
                    color='anomalo',
                    featureidkey='properties.UF_05',
                    scope='south america',
                    color_continuous_scale='ylorrd'
                    )
fig.update_layout(margin={"r": 0, "t": 0, "l": 0,
                          "b": 0}, clickmode='event+select')

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

        dash_table.DataTable(
            id='table',
            columns=[
                {'name': 'Data', 'id': 'data'},
                {'name': 'Estado', 'id': 'estado'},
                {'name': 'Compra', 'id': 'nome'},
                {'name': 'Preço', 'id': 'preco'},
                {'name': 'Quantidade', 'id': 'quantidade'},
            ],
            column_selectable='multi',
            data=df.assign(
                **df.select_dtypes(['datetime']).astype(str).to_dict('list')
            ).to_dict('records'),
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'fontSize': '18px',
            },
            style_cell={'textAlign': 'center'},
            style_cell_conditional=[
                {
                    'if': {'column_id': 'data'},
                    'width': '63px',
                    'minWidth': '63px',
                    'maxWidth': '63px'
                },
                {
                    'if': {'column_id': 'estado'},
                    'width': '63px',
                    'minWidth': '63px',
                    'maxWidth': '63px'
                },
                {
                    'if': {'column_id': 'nome'},
                    'width': '400px',
                    'minWidth': '400px',
                    'maxWidth': '400px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                },
                {
                    'if': {'column_id': 'preco'},
                    'width': '75px',
                    'minWidth': '75px',
                    'maxWidth': '75px'
                },
                {
                    'if': {'column_id': 'quantidade'},
                    'width': '63px',
                    'minWidth': '63px',
                    'maxWidth': '63px'
                },
                {
                    'if': {'column_id': 'anomalo'},
                    'width': '0px',
                    'minWidth': '0px',
                    'maxWidth': '0px'
                },
            ],
            style_data_conditional=[
                {
                    'if': {'column_id': 'nome'},
                    'textAlign': 'left',
                },
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                },
                {
                    'if': {'row_index': 'even'},
                    'backgroundColor': 'rgb(230, 230, 230)'
                },
                {
                    'if': {'filter_query': '{{anomalo}} = {}'.format(-1),
                           'row_index': 'odd'},
                    'backgroundColor': 'rgb(255, 205, 208)'
                },
                {
                    'if': {'filter_query': '{{anomalo}} = {}'.format(-1),
                           'row_index': 'even'},
                    'backgroundColor': 'rgb(255, 186, 191)'
                },
                {
                    'if': {'filter_query': '{Data} = NaT'},
                    'content': 'Sem data definida'
                }
            ],
            tooltip_data=[
                {
                    'nome': {'value': row['nome'], 'type': 'markdown'}
                } for row in df.to_dict('rows')
            ],
            tooltip_duration=None,
            style_as_list_view=True,
        ),
        
        html.P(
            'Caso você deseje conferir a tabela por completo, basta clicar no botão abaixo.',
            style={
                'color': 'rgba(255,255,255,0.9)',
                'marginTop' : '2%'
            }
        ),
        html.Div(
            className='button-parent',
            children=[
                html.A(
                    'Redirecionar',
                    id='redirect',
                    className='btn btn-primary',
                    href='/data'
                )
            ]
        )
    ]
)
