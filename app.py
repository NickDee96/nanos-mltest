import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_bootstrap_components as dbc
from main import main_func

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.LUX],
                suppress_callback_exceptions=True)

server = app.server



app.title="Nanos Machine Learning Test"

server = app.server
app.layout =dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.H1(
                children="Word Relevance Extractor",
                style={
                    "align":"center"
                }
            )
        ],width={"size": 6, "offset": 4})
    ]),
    dbc.Row([
        dbc.Col([
            dbc.FormGroup(
                [
                    dbc.Label("Enter the URL to be crawled below"),
                    dbc.Input(placeholder="URL goes here...", type="text",id = "url",),
                    dbc.FormText("e.g http://www.example.com/index.html"),
                ]
            )
        ],width={"size": 6, "offset": 4})
    ]),
    dbc.Row([
        dbc.Col([
            dbc.FormGroup(
                [
                    dbc.Label("Enter the list of products or services to match below separated by a comma"),
                    dbc.Input(placeholder="Keywords go here...", type="text",id = "keywords",),
                    dbc.FormText("e.g digital marketing, digital marketing tool"),
                ]
            )
        ],width={"size": 6, "offset": 4})
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Button("Submit",id = "submit", outline=True, color="primary", className="mr-1"),
        ],width={"size": 6, "offset": 4})
    ]),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.Div(id = "out")
        ],width={"size": 6, "offset": 4})
    ]),    
], fluid=True)

@app.callback(
    [Output("out","children")],
    [Input("submit","n_clicks")], 
    [State("url","value"),
    State("keywords","value")]
)
def get_output(n_clicks,url,keywords):
    if n_clicks:
        search_words = [x.strip() for x in keywords.split(",")]
        similar_words, fig = main_func(url,search_words)
        return [
            html.Div([
                html.H3(
                    children = f"Similar words to {keywords} are :"
                ),
                html.Div([html.Li(x) for x in similar_words]),
                dcc.Graph(
                    figure = fig
                )
            ])
        ]
    else:
        return [None]
if __name__ == "__main__":
    app.run_server(debug=True)