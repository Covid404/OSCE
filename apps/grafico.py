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
    'background': '#23272c',
    'text': 'black'
}

df = pd.read_csv('data/predictions.csv')
df['data'] = pd.to_datetime(df['data'])
current_year = 2020

fig = px.choropleth(df,
                    geojson=geojson_uf,
                    locations='estado',
                    color='anomalo',
                    featureidkey='properties.UF_05',
                    scope='south america'
                    )
fig.update_layout(margin={"r": 0, "t": 0, "l": 0,
                        "b": 0}, clickmode='event+select')

previous_click = None

layout = html.Div(
    children=[
        html.H1(
            id='dados-estado',
            children='Dados',
            style={'textAlign': 'center',
                    'color': 'rgba(255,255,255,0.90)'}
        ),

        html.Div(
            'Compras de Respiradores',
            style={'textAlign': 'center',
                    'marginTop': '1%',
                    'color': 'rgba(255,255,255,0.90)'}
        ),

        html.Div(
            id="map_geo_outer",
            className="map-container",
            children=[
                dcc.Graph(
                    id="choropleth",
                    figure=fig,
                ),
            ]
        ),

        html.Div(
            className='selectors-parent',
            children=[
                html.Div(
                    className="date-selector",
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
                            style={'color' : 'white'}
                        ),
                    ],
                ),
                html.Div(
                    className='price-slider-parent',
                    children=[
                        html.Span(
                            'Faixa de Preço: R$ %s - R$ %s' % (
                                df['preco'].min(), df['preco'].max()),
                            id='display-price-slider',
                            className="price-span",
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
                    className='amount-slider-parent',
                    children=[
                        html.Span(
                            'Quantidade: %s - %s' % (df['quantidade'].min(),
                                                    df['quantidade'].max()),
                            id='display-amount-slider'
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
            style={'textAlign': 'center'},
            className="table-parent",
            children=[
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
                        'fontSize' : '18px',
                    },
                    style_cell={'textAlign': 'center'},
                    style_cell_conditional=[
                        {
                            'if': {'column_id': 'data'},
                            'width': '102px',
                            'minWidth': '102px',
                            'maxWidth': '102px'
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
                            'if': {'row_index' : 'odd'},
                            'backgroundColor' : 'rgb(248, 248, 248)'
                        },
                        {
                            'if': {'row_index' : 'even'},
                            'backgroundColor' : 'rgb(230, 230, 230)'
                        },
                        {
                            'if': {'filter_query': '{{anomalo}} = {}'.format(-1),
                                    'row_index' : 'odd'},
                            'backgroundColor' : 'rgb(255, 205, 208)'
                        },
                        {
                            'if': {'filter_query': '{{anomalo}} = {}'.format(-1),
                                    'row_index' : 'even'},
                            'backgroundColor' : 'rgb(255, 186, 191)'
                        },
                    ],
                    tooltip_data=[
                        {
                            'nome': {'value': row['nome'], 'type': 'markdown'}
                        } for row in df.to_dict('rows')
                    ],
                    tooltip_duration=None,
                    style_as_list_view=True,
                )
            ]
        )
    ])


def update_datatable(start_date, end_date, price_limit, amount_limit, state_click):

    if state_click is not None:
        states = [point['location'] for point in state_click['points']]
        updated_df = df[df['estado'].isin(states)]
    else:
        updated_df = df

    start_date = dt.strptime(start_date, '%Y-%m-%d')
    end_date = dt.strptime(end_date, '%Y-%m-%d')
    updated_df = updated_df[
        (updated_df['data'] >= start_date)
        & (updated_df['data'] <= end_date)
    ]

    updated_df = updated_df[
        (updated_df['preco'] >= price_limit[0])
        & (updated_df['preco'] <= price_limit[1])
    ]

    updated_df = updated_df[
        (updated_df['quantidade'] >= amount_limit[0])
        & (updated_df['quantidade'] <= amount_limit[1])
    ]

    updated_df = updated_df.assign(
        **updated_df.select_dtypes(['datetime']).astype(str).to_dict('list')
    ).to_dict("rows")
    return updated_df


@app.callback(
    Output('table', 'data'),
    [
        Input('date-picker', 'start_date'),
        Input('date-picker', 'end_date'),
        Input('price-slider', 'value'),
        Input('amount-slider', 'value'),
        Input('choropleth', 'selectedData')
    ],
)
def update_data(start_date, end_date, price_limit, amount_limit, state_click):
    data = update_datatable(
        start_date[:10], end_date[:10], price_limit, amount_limit, state_click)
    return data


@app.callback(
    Output('display-price-slider', 'children'),
    [Input('price-slider', 'value')]
)
def update_price_slider(limits):
    return 'Faixa de Preço: %sR$ - %sR$' % (limits[0], limits[1])


@app.callback(
    Output('display-amount-slider', 'children'),
    [Input('amount-slider', 'value')]
)
def update_price_slider(limits):
    return 'Quantidade: %s - %s' % (limits[0], limits[1])
