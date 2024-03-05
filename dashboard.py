import dash
from dash import html, dcc
import pandas as pd  # Assuming you'll use Pandas for data
import plotly.express as px
from backend.data_processing import  count_missing_data

print("Dash Server Starting...")
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children="My Data Profiling Dashboard"),

    dcc.Graph(id='missing-data-heatmap')  # Placeholder for the heatmap
])

@app.callback(
    dash.Output('missing-data-heatmap', 'figure'),
    [dash.Input('some-trigger', 'value')]  # Placeholder trigger – we'll use ZeroMQ later
)
def update_heatmap(message):
    # ... Load data if needed ...
    df = pd.read_json(message)  # Example data source

    # Assuming you have your missing data logic ready
    missing_data = count_missing_data(df) 

    fig = px.imshow(missing_data, color_continuous_scale='Viridis', 
                    title="Missing Data Heatmap")
    return fig

