import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app


layout = html.Div([
        html.H1(
            children='Quem Somos',
            style={
                'textAlign': 'center',
                'color' : 'rgba(255,255,255,0.9)'
            }
        ),
        html.Div(
            'Equipe 06: Covid404 - Hackaton Serpro 2020',
            style={
                'textAlign': 'center',
                'color' : 'rgba(255,255,255,0.9)'
            }
        ),
        html.P(),
        html.Ul(children=[
            html.Li(children=[html.B('CEO: '),
            html.A(href='https://github.com/aianshay',children="Aian Shay")]),
            html.Li(children=[html.B('Web Dev: '),
            html.A(href='https://github.com/a-skz',children="Alberto Sobrinho")]),
            html.Li(children=[html.B('Web Dev: '),
            html.A(href='https://github.com/Arouck',children="Pedro Arouck")]),
            html.Li(children=[html.B('Data Analyst: '),
            html.A(href='https://github.com/renan-cunha',children="Renan Cunha")]),
            html.Li(children=[html.B('Data Analyst: '),
            html.A(href='https://github.com/Rjlmota',children="Renato Mota")])],
                          style={'textAlign': 'center',
                'color' : 'rgba(255,255,255,0.9)'
            }),
        html.P(),
        html.Div(children=[
            f'Esse website foi desenvolvido durante o ', 
            html.A(children='Hackaton Serpro 2020 ',
                   href='https://www.serpro.gov.br/menu/quem-somos/eventos/hackserpro/hackserpro-online')],
            style={
                'textAlign': 'center',
                'color' : 'rgba(255,255,255,0.9)'
            }
        ),
])

