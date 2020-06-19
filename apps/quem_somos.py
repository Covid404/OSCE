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
])

