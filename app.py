import dash

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
]

app = dash.Dash('Covis - Dashboard', suppress_callback_exceptions=True)
server = app.server
