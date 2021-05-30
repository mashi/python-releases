import dash
import dash_core_components as dcc
import dash_html_components as html

from main import get_information, visualization

df = get_information()
fig = visualization(df)

app = dash.Dash()
app.layout = html.Div([dcc.Graph(figure=fig)])


if __name__ == "__main__":
    app.run_server(debug=True)
