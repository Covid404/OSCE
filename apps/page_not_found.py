import dash_core_components as dcc
import dash_html_components as html
from app import app

colors = {
    'background': '#343a40',
    'text': 'white'
}

layout = html.Div(
    className='font-weight-light',
    style={
        'color': colors['text'],
        'textAlign': 'center'
    },
    children=[
        html.H1(
            '404',
            style={
                'marginBottom' : '2%'
            }
        ),
        html.H4(
            'Página não encontrada',
            style={
                'marginBottom' : '2%'
            }
        ),
        html.P(
            'Por favor, retorne a página anterior ou escolha uma das opções acima'
        )
    ]
)
