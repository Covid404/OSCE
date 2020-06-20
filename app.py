import dash

app = dash.Dash('Covis - Dashboard', suppress_callback_exceptions=True)
app.title = 'COVIS'
server = app.server
