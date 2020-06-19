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
map_df = map_df.rename(columns={'anomalo': 'media de anomalia'})

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

anomaly_colors = []
for color in px.colors.sequential.YlOrRd:
    anomaly_colors += [
        color.replace(')', ',{})'.format(0.25)),
        color.replace(')', ',{})'.format(0.50)),
        color.replace(')', ',{})'.format(0.75)),
        color.replace(')', ',{})'.format(1))
    ]


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
        'quantidade': 'Unidades',
        'anomalo': 'Anomalia'
    })

    updated_df = updated_df.assign(
        **updated_df.select_dtypes(['datetime']).astype(str).to_dict('list')
    )
    return updated_df


def get_anomaly_color(value):
    color_index = 0
    anomaly = 0
    while anomaly < value and color_index < 35:
        anomaly += 0.277
        color_index += 1

    return anomaly_colors[color_index]


def create_row(row):
    tr_children = []
    for index, value in row.iteritems():
        if index not in ['Fonte', 'anomalo_label']:
            if index == 'Compra':
                tr_children.append(
                    html.Td(
                        style={
                            'fontSize': 'small',
                            'textAlign': 'center',
                            'width': '70%'
                        },
                        children=[
                            value, ' (', html.A('Fonte', href=row['Fonte']), ')']
                    )
                )
            elif index == 'Anomalia':
                tr_children.append(
                    html.Td(
                        title='Nível: {}\nStatus: {}'.format(value, row['anomalo_label']),
                        children=html.Div(
                            className='progress',
                            style={
                                'backgroundColor': '#cfcfcf'
                            },
                            children=html.Div(
                                className='progress-bar',
                                style={
                                    'width': '{}%'.format(value*10),
                                    'backgroundColor': get_anomaly_color(value)
                                },
                                role="progressbar",
                                **{
                                    'aria-valuenow': "{}".format(value*10),
                                    'aria-valuemin': "0",
                                    'aria-valuemax': "100"
                                }
                            )
                        )
                    )
                )
            elif index == 'Data':
                if row['Data'] == 'NaT':
                    unknown_date = 'Sem data definida'
                    tr_children.append(
                        html.Td(
                            style={'fontSize': 'small', 'textAlign': 'center'},
                            children=unknown_date
                        )
                    )
                else:
                    olddate = dt.strptime(row['Data'], '%Y-%m-%d')
                    newdate = str(olddate.strftime('%d/%m/%Y'))
                    tr_children.append(
                        html.Td(
                            style={'fontSize': 'small', 'textAlign': 'center'},
                            children=newdate
                        )
                    )
            elif index == 'Preço/Unidade':
                value = '%.2f' % value
                preco = list(str(value)[::-1])[3:]
                decimal = list(str(value)[::-1])[:2]
                decimal.reverse()
                for i in range(len(preco) - 1):
                    if i != 0 and i % 3 == 0:
                        preco.insert(i, '.')
                preco.reverse()
                formated_value = 'R$ %s,%s ' % (
                    ''.join(preco), ''.join(decimal))
                tr_children.append(
                    html.Td(
                        style={'fontSize': 'small', 'textAlign': 'center'},
                        children=formated_value
                    )
                )
            else:
                tr_children.append(
                    html.Td(
                        style={'fontSize': 'small', 'textAlign': 'center'},
                        children=value
                    )
                )

    return html.Tr(children=tr_children)


def update_table(df):
    return html.Table(
        className='table table-sm table-hover',
        style={'backgroundColor': 'white'},
        children=[
            html.Thead(
                className='thead-light',
                children=html.Tr(
                    [
                        html.Th(column, style={
                                'fontSize': 'small', 'textAlign': 'center'})
                        for column in df.columns if column not in ['Fonte', 'anomalo_label']
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
        html.H3(
            id='dados-estado',
            children='Dados de Compras de Respiradores',
            style={
                'textAlign': 'center',
                'color': colors['text'],
                'marginTop': '1%'
            }
        ),

        html.Div(
            className='row row-cols-1 row-cols-md-3 mt-5',
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
                        html.Div(
                            html.Span(
                                'Faixa de Preço: R$ %s - R$ %s' % (
                                    df['preco'].min(), df['preco'].max()),
                                id='display-price-slider',
                                className="price-span",
                            ),
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
                    className='col text-center',
                    children=[
                        html.Div(
                            html.Span(
                                'Quantidade: %s - %s' % (df['quantidade'].min(),
                                                         df['quantidade'].max()),
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
            ]
        ),

        html.Div(
            className='d-flex justify-content-center mt-3',
            style={
                'minHeight': '66vh'
            },
            children=[
                html.Div(
                    className='row',
                    style={
                        'width': '98%',
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
                                'maxHeight': '66vh',
                                'overflow': 'auto'
                            },
                        ),
                    ]
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
    updated_df = update_dataframe(
        df, start_date[:10], end_date[:10], price_limit, amount_limit, state_clicked)
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
