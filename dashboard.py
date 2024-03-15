import dash
from dash import dcc, html
import plotly.figure_factory as ff
from plotly.graph_objects import Bar
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import zmq
from backend.data_processing import count_missing_data, investigate_dtype, count_duplicate_data, count_unique_values
from io import StringIO
import matplotlib.pyplot as plt



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

#Create a stacked bar chart to show the differnet data types in each column of the dataframe.
investigate_dtype_df = investigate_dtype(df)
data_types = investigate_dtype_df.columns
#print(investigate_dtype_df)
# Define a color mapping for data types
color_mapping = {
    'int': 'blue',
    'float': 'orange',
    'str': 'purple',
    'datetime': 'yellow',
    'Timestamp': 'yellow',
    'char': 'teal',
    'other': 'brown',
    'NoneType':'grey',
}

# Create a trace for each data type
traces = []
for dtype in data_types:
    traces.append(Bar(
        x=investigate_dtype_df.index,  # column names
        y=investigate_dtype_df[dtype],  # proportion of dtype in each column
        name=str(dtype),  # data type name
        marker_color=color_mapping.get(dtype, 'grey')  # use color mapping, default to 'grey' if dtype not in mapping
    ))

# Create the layout
layout = {
    'barmode': 'stack',
    'title': 'Data Types by Column'
}

# Create the figure
figure = {
    'data': traces,
    'layout': layout
}

# Create a heatmap
heatmap = ff.create_annotated_heatmap(z=missing_data_df.values, colorscale='Viridis', x=list(missing_data_df.columns), y=["Missing Values"], showscale=True)

# Unique values bar chart
unique_counts = count_unique_values(df).sort_values()

# Create a bar chart
bar_chart = go.Figure(data=[
    go.Bar(
        x=unique_counts.index,  # column names
        y=unique_counts.values,  # unique counts
    )
])

# Set layout
bar_chart.update_layout(
    title='Number of Unique Values by Column',
    xaxis_title='Columns',
    yaxis_title='Unique Count'
)



app.layout = html.Div(children=[
    html.H1(children='Data Profiling Dashboard'),
    dcc.Graph(figure=heatmap),
    dcc.Graph(id='graph', figure=figure),
    dcc.Graph(id='unique_bar_chart', figure=bar_chart),
    ])