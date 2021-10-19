import dash
from dash import dcc, html

from main import get_information, visualization

df = get_information()
fig = visualization(df)

app = dash.Dash()
app.layout = html.Div([dcc.Graph(figure=fig)])
server = app.server


if __name__ == "__main__":
    app.run_server(debug=True)
