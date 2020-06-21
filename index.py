import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from app import server
from apps import grafico, quem_somos, principal, como_funciona, page_not_found


app.layout = html.Div([
    html.Nav(
        className='navbar navbar-expand-lg navbar-dark bg-dark',
        children=[
            html.Div(
                id='navbarNav',
                children=[
                    html.Div(
                        className='navbar-nav',
                        children=[
                            html.A(
                                className='nav-brand',
                                href='/',
                                children=html.Img(
                                    className='d-inline-block align-top',
                                    src='assets/logo.svg',
                                    width=40,
                                    height=35
                                )
                            ),
                            html.A(
                                'Observatório',
                                className='nav-item nav-link',
                                href='/data'
                            ),
                            html.A(
                                'Sobre',
                                className='nav-item nav-link',
                                href='/sobre',
                            ),
                            html.A(
                                'Quem somos',
                                className='nav-item nav-link',
                                href='/quem_somos',
                            ),
                        ]
                    )
                ]
            )
        ]
    ),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', className='container')
])


@app.callback(Output('page-content', 'children'),
                [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return principal.layout
    elif pathname == '/quem_somos':
        return quem_somos.layout
    elif pathname == '/data':
        return grafico.layout
    elif pathname == '/sobre':
        return como_funciona.layout
    else:
        return page_not_found.layout

if __name__ == '__main__':
    app.run_server(debug=True)