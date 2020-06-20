import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
from datetime import date
import pandas as pd
import dash_table
from app import app
from apps import grafico

df = pd.read_csv('data/predictions.csv')
df['data'] = pd.to_datetime(df['data'])
current_year = 2020

df = df.sort_values('anomalo', ascending=False)[:5]

colors = {
    'background': '#343a40',
    'text': 'white'
}


def update_table(df):
    updated_df = grafico.update_dataframe(df, str(df['data'].min())[:10], str(df['data'].max())[
        :10], [0, df['preco'].max()], [0, df['quantidade'].max()], None)
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
                        for column in updated_df.columns if column not in ['Fonte', 'anomalo_label']
                    ]
                )
            ),
            html.Tbody(
                [grafico.create_row(row)
                    for index, row in updated_df.iterrows()]
            ),
        ]
    )


layout = html.Div(
    style={'textAlign': 'center'},
    className="table-parent",
    children=[
        html.Div(
            className='presentation-text-container',
            children=[
                html.H2(
                    'COVIS - Sistema de rastreamento de fraude',
                    style={
                        'color': 'rgba(255,255,255,0.9)',
                        'marginBottom': '2%'
                    }
                ),
                html.Span(
                    'Bla bla bla bla - textinho do ASIAN CEO',
                    style={
                        'color': 'rgba(255,255,255,0.9)',
                        'fontSize': '20px',
                        'fontWeight': '500'
                    }
                )
            ],
            style={
                'marginBottom': '2%'
            }
        ),

        html.H3(
            'Top 5 Fraudes',
            style={
                'color': '#ff7070',
                'marginBottom': '2%'
            }
        ),

        html.Div(
            className='d-flex justify-content-center',
            children=[
                html.Div(
                    className='table-responsive table-striped',
                    children=update_table(df),
                    style={
                        'maxWidth': '70%',
                        'maxHeight': '50vh',
                        'overflow': 'auto',
                    },
                ),
            ]
        ),

        html.P(
            'Caso você deseje conferir a tabela por completo, basta clicar no botão abaixo.',
            style={
                'color': 'rgba(255,255,255,0.9)',
                'marginTop': '2%'
            }
        ),

        html.A(
            'Visualizar',
            id='redirect',
            className='btn btn-primary',
            href='/data'
        )
    ]
)
