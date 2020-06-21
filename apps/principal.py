import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from app import app
from apps import grafico
from components import utils, table

df = utils.get_df()
df['data'] = pd.to_datetime(df['data'])
current_year = 2020

top_df = df.sort_values('anomalo', ascending=False)[:5]

colors = {
    'background': '#343a40',
    'text': 'rgba(255,255,255,0.9)'
}

do_not_create = ['Fonte', 'anomalo_label', 'nome_original', 'id']
def create_top_table(df):
    renamed_df = utils.get_renamed_df(df)

    renamed_df = renamed_df.assign(
        **renamed_df.select_dtypes(['datetime']).astype(str).to_dict('list')
    )

    return html.Div(
        className='table-responsive',
        children=table.create_table(renamed_df, do_not_create)
    )

layout = html.Div(
    style={'textAlign': 'center'},
    children=[

        html.Div(
            className='presentation-text-container',
            style={'marginBottom': '2%'},
            children=[
                html.H2(
                    'Observatório de Compras Emergenciais',
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
                                    'Ranking - Compras mais suspeitas',
                                    style={
                                        'color': 'rgb(64, 64, 64)',
                                        'marginBottom': 0,
                                        'fontWeight': 'bold'
                                    }
                                )
                            ),

                            html.Div(
                                className='card-body',
                                children=create_top_table(top_df)
                            ),
                            
                            html.Div(
                                className='card-footer',
                                children=html.A(
                                    'Veja os Dados Completos',
                                    id='redirect',
                                    className='btn btn-primary btn-sm',
                                    href='/data'
                                ),
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
                                html.H4('As 5 compras mais suspeitas tiveram preço médio por unidade de'),
                                html.H4(
                                    utils.get_formated_price(top_df['preco'].mean()),
                                    style={'fontWeight': 'bold'}
                                ),
                                html.H4('Isso significa um possível superfaturamento de até'),
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
                        O Observatório é um sistema que utiliza uma 
                        Inteligência Artificial chamada IARA para
                        monitorar os gastos públicos no combate à
                        COVID-19. O Observatório preza pela
                        visualização simples e intuitiva dos gastos para os órgãos
                        fiscalizadores, ONGs, imprensa e sociedade civil.
                    '''
                ),
                html.Br(),
                html.H5(
                    className='text-center',
                    children=[
                        '''
                            A IARA é capaz de alertar um gasto suspeito,
                            destoante de todos os outros de mesmo tipo feitos pelo país.
                            Ele funciona consultando e analisando periodicamente os gastos das
                            secretarias estaduais. Clique 
                        ''',
                        html.A('AQUI', id='redirect', href='/sobre'),
                        ' para saber mais.'
                    ]
                ),
            ]
        ),

        html.Br(),
        html.Br(),
#        html.P( 
#            style={'color': colors['text']},
#            children='''
#                    Somos uma equipe de estudantes da Universidade Federal do
#                    Pará sem quaisquer fins lucrativos.
#                '''
#        ),
#
#        html.P(
#            style={'color': colors['text']},
#            children='''
#                Por esse motivo, necessitamos do seu apoio!
#            '''
#        ),
#
#        html.P(
#            style={'color': colors['text']},
#            children=[
#                'Clique ',
#                html.A('AQUI', id='redirect', href='/quem_somos'),
#                ' e veja como você pode fazer parte disso.'
#            ]
#        )

    ]
)
