import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from datetime import datetime as dt
from datetime import date, timedelta
from app import app
from dash.dependencies import Input, Output

colors = {
    'background': '#23272c',
    'text': 'black'
}

df = pd.read_csv('data/predictions.csv', infer_datetime_format=True)
df['data'] = pd.to_datetime(df['data'])
current_year = 2020

layout = html.Div(
    children=[
        html.H1(
            id='dados-estado',
            children='Dados',
            style={'textAlign': 'center'}
        ),
        
        html.Div(
            'Compras de Respiradores',
            style={'textAlign': 'center'}
        ),

        html.Div(
            className="row",
            style={'marginTop': 30, 'marginBottom': 0},
            children=[
                dcc.DatePickerRange(
                    id='date-picker',
                    display_format='D/M/Y',
                    min_date_allowed=df['data'].min(),
                    max_date_allowed=df['data'].max(),
                    initial_visible_month=dt(current_year,df['data'].max().month, 1),
                    start_date=df['data'].min(),
                    end_date=df['data'].max(),
                ),
            ],
        ),

        html.Div(
            className="row",
            style={'marginTop': 0, 'marginBottom': 0},
            children=[
                dcc.Dropdown(
                    id='state-picker',
                    options=[{'label':estado, 'value':estado} for estado in df['estado'].unique()],
                    multi=True,
                    placeholder='Selecione um Estado',
                    style={'width': '286px', 'heigth':'48px'},
                    value=[]
                ),
            ],
        ),

        html.Div(
            style={'marginTop': 15},
            children=[
                html.Span(
                    'Faixa de Preço: %sR$ - %sR$' % (df['preco'].min(), df['preco'].max()),
                    id='display-price-slider'
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
            children=[
                html.Span(
                    'Quantidade: %s - %s' % (df['quantidade'].min(), df['quantidade'].max()),
                    id='display-amount-slider'
                ),
                dcc.RangeSlider(
                    id='amount-slider',
                    min=df['quantidade'].min(),
                    max=df['quantidade'].max(),
                    step=1,
                    value=[df['quantidade'].min(), df['quantidade'].max()],
                )
            ]
        ),

        html.Div(
            style={'textAlign': 'center'},
            children=[
                dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in df.columns],
                    column_selectable='multi',
                    data=df.assign(
                        **df.select_dtypes(['datetime']).astype(str).to_dict('list')
                    ).to_dict('records'),
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
                            'width': '102px',
                            'minWidth': '102px',
                            'maxWidth': '102px'
                        },
                        {
                            'if': {'column_id': 'quantidade'},
                            'width': '102px',
                            'minWidth': '102px',
                            'maxWidth': '102px'
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
                            'if':{'column_id': 'nome'},
                            'textAlign': 'left',
                        },
                        {
                            'if':{'filter_query': '{{anomalo}} = {}'.format(-1),},
                            'backgroundColor': '#fff3cd',
                        },
                    ],
                    tooltip_data=[
                        {
                            'nome': {'value': row['nome'], 'type': 'markdown'}
                        } for row in df.to_dict('rows')
                    ],
                    tooltip_duration=None,
                )
            ]
        )
])


def update_datatable(start_date, end_date, states, price_limit, amount_limit):
    if start_date is not None:
        start_date = dt.strptime(start_date, '%Y-%m-%d')
    if end_date is not None:
        end_date = dt.strptime(end_date, '%Y-%m-%d')
    updated_df = df[(df['data'] >= start_date) & (df['data'] <= end_date)]

    if states != []:
        updated_df = updated_df[updated_df['estado'].isin(states)]

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
        Input('state-picker', 'value'),
        Input('price-slider', 'value'),
        Input('amount-slider', 'value')
    ]
)
def update_data(start_date, end_date, states, price_limit, amount_limit):
	data = update_datatable(start_date[:10], end_date[:10], states, price_limit, amount_limit)
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