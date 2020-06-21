import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app

slides = [
    html.Div(
        className='item-container',
        children=[
            html.Div(
                children=[
                    html.Img(
                        className='img-fluid',
                        style={
                            'marginBottom': '2%'
                        },
                        src='assets/web-scr.jpg'
                    ),

                    html.P(
                        children=['''
                                    Técnica que consiste em extrair os dados de
                                ''',
                                  html.Span(
                                      'websites',
                                      className='font-italic'
                                  ),
                                  '''
                                    automaticamente.
                                    No caso do Observatório, os dados são extraídos dos portais de transparência estaduais,
                                    então foi necessário criar um programa específico para cada portal.
                                    Nessa etapa, utilizamos a ferramenta
                                ''',
                                  html.Span(
                                      'Selenium.',
                                      className='font-italic'
                                  )
                                  ]
                    )
                ],
            ),
        ]
    ),
    html.Div(
        className='item-container',
        children=[
            html.Div(
                children=[
                    html.Img(
                        className='img-fluid',
                        style={
                            'marginBottom': '2%'
                        },
                        src='assets/data-wra.jpg'
                    ),
                    html.P(
                        children=['''
                            Com os dados obtidos, agora fazemos a limpeza, selecionamos os dados apenas de
                            ventiladores, obtemos os valores de compras e deixamos em um formato utilizável.
                            Nessa etapa, utilizamos as ferramentas
                            ''',
                                  html.Span(
                                      'Pandas',
                                      className='font-italic'
                                  ),
                                  ' e ',
                                  html.Span(
                                      'Numpy',
                                      className='font-italic'
                                  ),
                                  '.'
                                  ]
                    )
                ]
            ),
        ],
    ),
    html.Div(
        className='item-container',
        children=[
            html.Div(
                children=[
                    html.Img(
                        className='img-fluid',
                        style={
                            'marginBottom': '2%'
                        },
                        src='assets/machine-learning.jpg'
                    ),
                    html.P(
                        children=['''
                            Aqui é onde é feita a detecção de anomalias a partir dos dados obtidos.
                            O algoritmo que utilizamos é o
                        ''',
                                  html.Span(
                                      'Minimum Covariance Determinant Estimator,',
                                      className='font-italic'
                                  ),
                                  '''
                            que detecta
                        ''',
                                  html.Span(
                                      'outliers',
                                      className='font-italic'
                                  ),
                                  '''
                            (exemplos que fogem do padrão)
                            em conjuntos de dados que estão distribuidos de forma normal. Para isso,
                            utilizamos a biblioteca
                        ''',
                                  html.Span(
                                      'Scikit-Learn',
                                      className='font-italic'
                                  ),
                                  '.'
                                  ]
                    )
                ]
            ),
        ],
    ),
    html.Div(
        className='item-container',
        children=[
            html.Div(
                children=[
                    html.Img(
                        className='img-fluid',
                        style={
                            'marginBottom': '2%'
                        },
                        src='assets/web-dev.jpg'
                    ),
                    html.P(
                        children=['''
                            Parte em que é feita a apresentação de dados de forma acessível. Os dados são
                            apresentados no formato de tabelas e
                        ''',
                                  html.Span(
                                      'heatmap,',
                                      className='font-italic'
                                  ),
                                  '''
                            com cores que indicam
                            características dos dados, como quão suspeita é uma compra. Utilizamos aqui
                            o
                        ''',
                                  html.Span(
                                      'framework',
                                      className='font-italic'
                                  ),
                                  '''
                            de desenvolvimento web
                        ''',
                                  html.Span(
                                      'Dash',
                                      className='font-italic'
                                  ),
                                  '''
                            e a biblioteca
                        ''',
                                  html.Span(
                                      'Plotly',
                                      className='font-italic'
                                  ),
                                  '''
                            para
                            visualização de dados.
                        '''
                                  ]
                    )
                ]
            ),
        ]
    )
]

layout = [
    html.H3(
        style={
            'textAlign': 'center',
            'color': 'rgba(255,255,255,0.9)',
            'marginBottom': '2%'
        },
        children='Sobre'
    ),


    html.P(
        style={'textAlign': 'justify', 'color': 'rgba(255,255,255,0.9)'},
        children='''
            O Observatório usa diversas técnicas e tecnologias para monitorar 
            as compras (apenas de ventiladores pulmonares por enquanto) e 
            determinar o nível de anomalia de cada compra, o chamado 
            suspeitômetro. O sistema determina o quanto cada compra é 
            suspeita, e não se houve realmente fraude. A tarefa de verificação
            de fraude deve ser feita através de um trabalho investigativo, o 
            qual não é o papel do Observatório. O papel do sistema é agilizar 
            o processo investigativo informando aos agentes fiscalizadores 
            quais compras possuem uma maior probabilidade de serem irregulares.
        '''
    ),

    html.P(
        style={
            'textAlign': 'justify',
            'color': 'white',
            'marginBottom': '2%',
        },
        children=[
            '''
            As técnicas utilizadas para o desenvolvimento do sistema são:
            ''',
            html.Span(
                'web scraping',
                className='font-italic'
            ),
            ', ',
            html.Span(
                'data wrangling',
                className='font-italic'
            ),
            ', ',
            html.Span(
                'machine learning',
                className='font-italic'
            ),
            ' e ',
            html.Span(
                'web development',
                className='font-italic'
            ),
            '.',
            '''
            Essas técnicas foram transformadas em módulos, que são executados em sequência
            de acordo com o slide abaixo. Toda a solução foi implementada na linguagem de programação
            ''',
            html.Span(
                'Python',
                className='font-italic'
            ),
            '.'
        ]
    ),

    html.Div(
        className='d-flex justify-content-center',
        children=[
            html.Div(
                className='d-flex justify-content-center',
                style={
                    'textAlign': 'center',
                    'width': '100%',
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                },
                children=[
                    html.H2(
                        '<',
                        id='prev_slide',
                        className='button_slider',
                        style={
                            'color': '#25282b',
                            'marginRight': '2%'
                        }
                    ),
                    html.Div(
                        children=html.Div(
                            className="d-flex justify-content-center",
                            children=[
                                html.Div(
                                    id='slide',
                                    style={
                                        'backgroundColor': 'white',
                                        'width': '1000px',
                                        'height': '500px',
                                        'padding': '2%',
                                        'borderRadius': '10px',
                                        'overflow': 'hidden'
                                    },
                                ),
                            ]
                        )
                    ),
                    html.H2(
                        '>',
                        id='prox_slide',
                        className='button_slider',
                        style={
                            'color': '#25282b',
                            'marginLeft': '2%'
                        }
                    ),
                ]
            )
        ]
    ),
    html.P(),

    html.H2(children="Fontes dos Dados",
            style={
                    'textAlign': 'center',
                    'color': 'rgba(255,255,255,0.9)',
                    'marginBottom' : '2%',
                    'marginTop' : '2%'
                }
            ),

    html.Ul(children=[
            html.Li(children=[html.A(href='http://transparencia.al.gov.br/despesa/despesas-com-covid19/',
                                     children="AL")]),
            html.Li(children=[html.A(href='http://www.transparencia.ap.gov.br/consulta/2/496/despesas/',
                                     children="AP")]),
            html.Li(children=[html.A(href='http://www.saude.ba.gov.br/temasdesaude/coronavirus/contratacoes-covid19/',
                                     children="BA")]),
            html.Li(children=[html.A(href='https://www.comprasgovernamentais.gov.br/index.php/transparencia/60-transparencia/1313-transparencia-dos-dados-de-compras-para-o-covid-19',
                                     children="BR")]),
            html.Li(children=[html.A(href='https://cearatransparente.ce.gov.br/portal-da-transparencia/paginas/coronavirus-despesas',
                                     children="CE")]),
            html.Li(children=[html.A(href='https://coronavirus.es.gov.br/contratos-emergenciais',
                                     children="ES")]),
            html.Li(children=[html.A(href='http://www.transparencia.dadosabertos.mg.gov.br/dataset/contratacoes-coronavirus',
                                     children="MG")]),
            html.Li(children=[html.A(href='http://www.comprascoronavirus.ms.gov.br/',
                                     children="MS")]),
            html.Li(children=[html.A(href='http://www.transparencia.mt.gov.br/-/contratos-covid-19',
                                     children="MT")]),
            html.Li(children=[html.A(href='https://transparenciacovid19.pa.gov.br/covid.json',
                                     children="PA")]),
            html.Li(children=[html.A(href='https://comprasemergenciaiscovid19.saude.pe.gov.br/',
                                     children="PE")]),
            html.Li(children=[html.A(href='https://sistemas.tce.pi.gov.br/contratosweb/mural/?s=covid',
                                     children="PI")]),
            html.Li(children=[html.A(href='http://www.transparencia.pr.gov.br/pte/compras/dispensasInexigibilidade?windowId=adf',
                                     children="PR")]),
            html.Li(children=[html.A(href='http://painel.saude.rj.gov.br/contratos/transparencia.html',
                                     children="RJ")]),
            html.Li(children=[html.A(href='http://transparencia.rn.gov.br/covid',
                                     children="RN")]),
            html.Li(children=[html.A(href='http://www.transparencia.ro.gov.br/Grafico/DespesasCOVID19',
                                     children="RO")]),
            html.Li(children=[html.A(href='http://www.transparencia.rr.gov.br/index.php/roraima-contra-o-coronavirus/consulta-despesas-covid19',
                                     children="RR")]),
            html.Li(children=[html.A(href='https://www.saopaulo.sp.gov.br/coronavirus/transparencia/',
                                     children="SP")]),
            ], style={'textAlign': 'center',
                      'color': 'rgba(255,255,255,0.9)'
                      }),

]


@app.callback(Output('slide', 'children'),
              [
    Input('prev_slide', 'n_clicks'),
    Input('prox_slide', 'n_clicks')
])
def display_prev_slide(prev, prox):
    if prev == None and prox == None:
        return slides[0]
    else:
        if prev == None:
            prev = 0
        if prox == None:
            prox = 0
        new_index = (prox - prev) % 4
        return slides[new_index]

# @app.callback(Output('slide', 'children'),
#               [Input('interval', 'n_intervals')])
# def display_prox_slide(n):
#     if n == None:
#         n = 1
#     else:
#         n = n + 1
#     print(n)
#     if n % 4 == 1:
#         slide =
#     elif n % 4 == 2:
#         slide =
#     elif n % 4 == 3:
#         slide =
#     elif n % 4 == 0:
#         slide =
#     else:
#         slide = "None"
#     return slide

# [     html.H3(
#         style={'textAlign': 'center', 'color': 'white'},
#         children='Como Funciona?'
#     ),

#     html.P(
#         style={'textAlign': 'justify', 'color': 'white'},
#         children='''
#             O COVIS usa diversas técnicas e tecnologias para monitorar as compras de
#             ventiladores e determinar o nível de anomalia de cada compra. O COVIS determina o quanto cada compra é suspeita, e não se houve realmente
#             fraude. A tarefa de verificação de fraude deve ser feita através de um trabalho
#             investigativo, o qual não é o papel do COVIS.
#         '''
#     ),

#     html.P(
#         style={'textAlign': 'justify', 'color': 'white'},
#         children='''
#             As técnicas utilizadas para o desenvolvimento do sistema são:
#             *web scraping*, *data wrangling*, *machine learning* e *web development*.
#             Essas técnicas foram transformadas em módulos, que são executados em sequência
#             de acorco com a figura abaixo. Toda a solução foi implementada na linguagem de programação
#             *Python*.
#         '''
#     ),

#     html.Img(
#         className='img-fluid',
#         src='assets/pipeline.jpeg'
#     ),

#     html.Br(),
#     html.Br(),

#     html.Div(
#         className='row',
#         children=[
#             html.Div(
#                 className='col',
#                 style={'textAlign': 'justify', 'color': 'white'},
#                 children=[
#                     html.H5(
#                         style={'textAlign': 'center'},
#                         children='Web Scrapping'
#                     ),

#                     html.P(
#                         '''
#                             Técnica que consiste em extrair os dados de *websites* de forma automática.
#                             No caso do COVIS, os dados são extraídos dos portais de transparência de cada
#                             estado, então foi necessário criar um programa específico para cada portal.
#                             Nessa etapa, utilizamos a ferramenta *Selenium*.
#                         '''
#                     )
#                 ]
#             ),

#             html.Div(
#                 className='col',
#                 style={'textAlign': 'justify', 'color': 'white'},
#                 children=[
#                     html.H5(
#                         style={'textAlign': 'center'},
#                         children='Data Wrangling'
#                     ),

#                     html.P(
#                         '''
#                             Com os dados obtidos, agora fazemos a limpeza, selecionamos os dados apenas de
#                             ventiladores, obtemos os valores de compras e deixamos em um formato utilizável.
#                             Nessa etapa, utilizamos as ferramentas *Pandas* e *Numpy*.
#                         '''
#                     )
#                 ]
#             )
#         ]
#     ),

#         html.Div(
#         className='row',
#         children=[
#             html.Div(
#                 className='col',
#                 style={'textAlign': 'justify', 'color': 'white'},
#                 children=[
#                     html.H5(
#                         style={'textAlign': 'center'},
#                         children='Machine Learning'
#                     ),

#                     html.P(
#                         '''
#                             Aqui é onde é feita a detecção de anomalias a partir dos dados obtidos.
#                             O algoritmo que utilizamos é o *Minimum Covariance
#                             Determinant Estimator*, que detecta *outliers* (exemplos que fogem do padrão)
#                             em conjuntos de dados que estão distribuidos de forma normal. Para isso,
#                             utilizamos a biblioteca *Scikit-Learn*
#                         '''
#                     )
#                 ]
#             ),

#             html.Div(
#                 className='col',
#                 style={'textAlign': 'justify', 'color': 'white'},
#                 children=[
#                     html.H5(
#                         style={'textAlign': 'center'},
#                         children='Web'
#                     ),

#                     html.P(
#                         '''
#                             Parte em que é feita a apresentação de dados de forma acessível. Os dados são
#                             apresentados no formato de tabelas e *heatmap*, com cores que indicam
#                             características dos dados, como quão suspeita é uma compra. Utilizamos aqui
#                             o *framework* de desenvolvimento web *Dash* e a biblioteca *Plotly* para
#                             visualização de dados.
#                         '''
#                     )
#                 ]
#             )
#         ]
#     )
# ]
