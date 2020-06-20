import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app

layout = [
    html.H3(
        style={'textAlign': 'center', 'color': 'white'},
        children='Como Funciona?'
    ),

    html.P(
        style={'textAlign': 'justify', 'color': 'white'},
        children='''
            O COVIS usa diversas técnicas e tecnologias para monitorar as compras de
            ventiladores e determinar o nível de anomalia de cada compra. O COVIS determina o quanto cada compra é suspeita, e não se houve realmente
            fraude. A tarefa de verificação de fraude deve ser feita através de um trabalho
            investigativo, o qual não é o papel do COVIS.
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
            de acorco com a figura abaixo. Toda a solução foi implementada na linguagem de programação
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
                    'textAlign': 'center'
                },
                children=html.Div(
                    className="carousel slide",
                    children=html.Div(
                        className="carousel-inner d-flex justify-content-center",
                        children=[
                            html.Div(
                                id='slide',
                                className='carousel-inner d-flex justify-content-center',
                                style={
                                    'backgroundColor': 'white',
                                    'width' : '60%',
                                    'padding' : '2%',
                                    'borderRadius' : '10px',
                                    'overflow' : 'hidden'
                                }
                            ),
                            dcc.Interval(id='interval', interval=5000),
                        ]
                    )
                )
            )
        ]
    ),
]


@app.callback(Output('slide', 'children'),
              [Input('interval', 'n_intervals')])
def display_slide(n):
    if n == None or n % 4 == 1:
        slide = html.Div(
            className='item-container',
            children=[
                html.Div(
                    className='carousel-item active',
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
                            No caso do COVIS, os dados são extraídos dos portais de transparência estaduais,
                            então foi necessário criar um programa específico para cada portal.
                            Nessa etapa, utilizamos a ferramenta
                        ''',
                                      html.Span(
                                          'Selenium',
                                          className='font-italic'
                                      ),
                                      '.'
                                      ]
                        )
                    ],
                ),

                html.Span(
                    '<'
                )
            ]
        ),
    elif n % 4 == 2:
        slide = html.Div(
            className='item-container',
            children=[
                html.Div(
                    className='carousel-item active',
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
        )
    elif n % 4 == 3:
        slide = html.Div(
            className='item-container',
            children=[
                html.Div(
                    className='carousel-item active',
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
        )
    elif n % 4 == 0:
        slide = html.Div(
            className='item-container',
            children=[
                html.Div(
                    className='carousel-item active',
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
    else:
        slide = "None"
    return slide

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
