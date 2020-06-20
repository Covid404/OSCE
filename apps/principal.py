import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
import pandas as pd
from app import app
from apps import grafico
import components.utils as utils

df = pd.read_csv('data/predictions.csv')
df['data'] = pd.to_datetime(df['data'])
current_year = 2020

top_df = df.sort_values('anomalo', ascending=False)[:5]

colors = {
    'background': '#343a40',
    'text': 'rgba(255,255,255,0.9)'
}

do_not_create = ['Fonte', 'anomalo_label', 'nome_original']
def create_top_five(df):
    renamed_df = utils.get_renamed_df(df)

    renamed_df = renamed_df.assign(
        **renamed_df.select_dtypes(['datetime']).astype(str).to_dict('list')
    )

    header_style = {'color':'#495057', 'fontSize': 'small', 'fontWeight': 'bold'}

    top_five_rows = [
        html.Div(
            className='row mb-2',
            style={'backgroundColor': '#e9ecef'},
            children=[
                html.Div('Compra', className='col p-1', style=header_style),
                html.Div('Unidades', className='col p-1', style=header_style),
                html.Div('Preço/Unidade', className='col p-1', style=header_style),
                html.Div('Data', className='col p-1', style=header_style),
                html.Div('Uf', className='col p-1', style=header_style),
                html.Div('Suspeitômetro', className='col p-1', style=header_style)
            ]
        )
    ]
    for index, row in renamed_df.iterrows():
        children = []
        for index, value in row.iteritems():
            if index not in do_not_create:
                if index == 'Compra':
                    children.append(
                        html.Div(
                            className='col p-1 d-block text-truncate',
                            style={
                                'fontSize': 'small',
                                'textAlign': 'center',
                            },
                            title=row['nome_original'],
                            children=value
                        )
                    )
                elif index == 'Suspeitômetro':
                    children.append(
                        html.Div(
                            className='col p-1',
                            title='Nível: {}\nAlerta: {}'.format(value, row['anomalo_label']),
                            children=html.Div(
                                className='progress',
                                style={'backgroundColor': '#cfcfcf'},
                                children=html.Div(
                                    className='progress-bar',
                                    style={
                                        'width': '{}%'.format(value*10),
                                        'backgroundColor': utils.get_anomaly_color(value)
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
                    children.append(
                        html.Div(
                            className='col p-1',
                            style={'fontSize': 'small', 'textAlign': 'center'},
                            children=utils.get_formated_date(value)
                        )
                    )
                elif index == 'Preço/Unidade':
                    children.append(
                        html.Div(
                            className='col p-1',
                            style={'fontSize': 'small', 'textAlign': 'center'},
                            children=utils.get_formated_price(value)
                        )
                    )
                else:
                    children.append(
                        html.Div(
                            className='col p-1',
                            style={'fontSize': 'small', 'textAlign': 'center'},
                            children=value
                        )
                    )

        top_five_rows.append(
            html.Div(
                className='row mb-2',
                children=children
            )
        )



    return top_five_rows

layout = html.Div(
    style={'textAlign': 'center'},
    children=[

        html.Div(
            className='presentation-text-container',
            style={'marginBottom': '2%'},
            children=[
                html.H2(
                    'COVIS - Sistema de Monitoramento de Compras Públicas',
                    style={'color': colors['text']}
                ),
            ],
        ),

        html.Div(
            className='row',
            children=[
                html.Div(
                    className='col-8',
                    children=html.Div(
                        className='card bg-light',
                        style={'height': '100%'},
                        children=[
                            html.Div(
                                className='card-header',
                                children=html.H4(
                                    'Top 5 Suspeitômetro',
                                    style={
                                        'color': 'rgb(255, 112, 112)',
                                        'marginBottom': 0,
                                        'fontWeight': 'bold'
                                    }
                                )
                            ),

                            html.Div(
                                className='card-body',
                                children=create_top_five(top_df)
                            )
                        ]
                    )
                ),

                html.Div(
                    className='col-4',
                    children=html.Div(
                        className='jumbotron p-3 mb-0',
                        style={'height': '100%'},
                        children=html.Div(
                            style={'margin': 'auto'},
                            children=[
                                html.H4('As 5 compras mais suspeitas tiveram média de'),
                                html.H4(
                                    utils.get_formated_price(top_df['preco'].mean()),
                                    style={'fontWeight': 'bold'}
                                ),
                                html.H4('o que significa um possível superfaturamento de até'),
                                html.H4(
                                    '{}%'.format(
                                        str(top_df['preco'].mean() / df['preco'].mean()*100)[:6],
                                    ),
                                    style={'fontWeight': 'bold'}
                                ),
                                html.H4('em relação à média nacional.')
                            ]
                        )
                    )
                )
            ]
        ),

        html.Br(),
        html.Br(),

        html.Div(
            className='jumbotron p-3 mb-0',
            children=[
                html.H5(
                    className='text-center',
                    children='''
                    O COVIS é um sistema que utiliza inteligência artificial para
                    fiscalizar os gastos públicos durante a pandemia e preza pela
                    visualização simples e intuitiva dos gastos para a sociedade civil,
                    ONGs, imprensa e até mesmo os órgãos fiscalizadores.
                    '''
                ),
                html.Br(),
                html.H5(
                    className='text-center',
                    children='''
                    Com a ciência de dados, o COVIS é capaz de alertar um gasto suspeito,
                    destoante de todos os outros de mesmo tipo feitos pelo país.
                    Ele funciona consultando e analisando periodicamente os gastos das
                    secretarias estaduais de todos os 27 estados da federação.
                    '''
                ),
            ]
        ),

        html.P(
            'Caso deseje conferir os dados por completo, basta clicar no botão abaixo.',
            style={
                'color': 'rgba(255,255,255,0.9)',
                'marginTop': '2%'
            }
        ),

        html.A(
            'Observatório',
            id='redirect',
            className='btn btn-primary',
            href='/data'
        )
    ]
)
