import dash_html_components as html
import components.utils as utils


def create_row(row, do_not_create):
    tr_children = []
    for index, value in row.iteritems():
        if index not in do_not_create:
            if index == 'Compra':
                tr_children.append(
                    html.Td(
                        style={
                            'fontSize': 'small',
                            'textAlign': 'center',
                        },
                        title=row['nome_original'],
                        children='{} - {}'.format(row['id'], value)
                    )
                )
            elif index == 'Suspeitômetro':
                tr_children.append(
                    html.Td(
                        title='Nível: {}\nAlerta: {}'.format(
                            value, row['anomalo_label']
                        ),
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
                tr_children.append(
                    html.Td(
                        style={'fontSize': 'small', 'textAlign': 'center'},
                        children=utils.get_formated_date(value)
                    )
                )
            elif index in ['Preço/Unidade', 'Preço Total']:
                tr_children.append(
                    html.Td(
                        style={'fontSize': 'small', 'textAlign': 'center'},
                        children=utils.get_formated_price(value)
                    )
                )
            else:
                tr_children.append(
                    html.Td(
                        style={'fontSize': 'small', 'textAlign': 'center'},
                        children=value
                    )
                )

    return html.Tr(children=tr_children, className='mb-2')

def create_table(df, do_not_create):
    return html.Table(
        className='table table-sm',
        style={'borderTop': 'none'},
        children=[
            html.Thead(
                className='thead-light',
                children=html.Tr(
                    [
                        html.Th(column, style={
                                'fontSize': 'small', 'textAlign': 'center'})
                        for column in df.columns if column not in do_not_create
                    ]
                )
            ),
            html.Tbody(
                [create_row(row, do_not_create) for index, row in df.iterrows()]
            ),
        ]
    )