import dash
from dash import dcc, html, dash_table
import plotly.figure_factory as ff
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import zmq
from backend.data_processing import count_missing_data, investigate_dtype
from io import StringIO



app = dash.Dash(__name__)

# Setup ZeroMQ to receive DataFrame
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5556")
print("Connected to server")
socket.setsockopt_string(zmq.SUBSCRIBE, '')

# Receive and print test message
test_message = socket.recv_string()
#print(test_message)

# Receive DataFrame from ZeroMQ
df_json = socket.recv_json()
#print(df_json)
df = pd.read_json(StringIO(df_json))

# Create a boolean DataFrame where True indicates a missing value
missing_data = count_missing_data(df)
missing_data = count_missing_data(df)
missing_data_df = missing_data.to_frame().T  # Convert Series to DataFrame and transpose
#print(missing_data)

investigate_dtype_df = investigate_dtype(df)
data = investigate_dtype_df.to_dict('records')

# Create a heatmap
heatmap = ff.create_annotated_heatmap(z=missing_data_df.values, colorscale='Viridis', x=list(missing_data_df.columns), y=["Missing Values"], showscale=True)

app.layout = html.Div(children=[
    html.H1(children="Hello"),
    html.P("This is a minimal Dash app for testing."),
    dcc.Graph(figure=heatmap),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in investigate_dtype_df.columns],
        data=data)])