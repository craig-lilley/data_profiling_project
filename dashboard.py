import dash
from dash import dcc, html, dash_table
import plotly.figure_factory as ff
from plotly.graph_objects import Bar
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import zmq
from backend.data_processing import count_missing_data, investigate_dtype, count_duplicate_data, count_unique_values, describe, outliers, most_common_values
from io import StringIO
import matplotlib.pyplot as plt


"""This Code is for setting up the Dash server and receiving the DataFrame from ZeroMQ."""
app = dash.Dash(__name__)

# Setup ZeroMQ to receive DataFrame
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5556")
print("Connected to server")
socket.setsockopt_string(zmq.SUBSCRIBE, '')

# Receive and print test message
file_type = socket.recv_string()
#print(test_message)

# Receive DataFrame from ZeroMQ
df_json = socket.recv_json()
#print(df_json)
df = pd.read_json(StringIO(df_json))


"""This Code provides the characteristics of the dataframe."""
# Define the characteristics
characteristics = {
    'File Type': file_type,
    'Number of Rows': df.shape[0],
    'Number of Columns': df.shape[1],
    'Number of Missing Values': df.isnull().sum().sum(),
    'Number of Duplicate Rows': count_duplicate_data(df),
}

# Convert the characteristics to a DataFrame
characteristics_df = pd.DataFrame.from_records([characteristics])

# Convert the DataFrame to a dictionary for the DataTable
data_dict = characteristics_df.to_dict('records')

# Create a title and a table for the dataset characteristics
characteristics_table = html.Div([
    html.H3('Dataset Characteristics'),
    dash_table.DataTable(
        id='characteristics_table',
        columns=[{"name": i, "id": i} for i in characteristics_df.columns],
        data=data_dict,
    )
])


"""This Code provides a sample of the data in the dataframe."""
# Get the first 5 rows of the dataframe
df_sample = df.head()

# Convert the dataframe to a dictionary for the DataTable
data_dict = df_sample.to_dict('records')

# Create a title and a table for the sample data
data_table = html.Div([
    html.H3('Sample of Data'),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df_sample.columns],
        data=data_dict,
    )
])


"""This Code is for investigating and visualiseing the missing data in the dataframe."""
missing_data = count_missing_data(df).sort_values(ascending=False)

missing_values_bar_chart = go.Figure(data=[
    go.Bar(
        x=missing_data.index,  # column names
        y=missing_data.values,  # number of missing values
        marker_color='blue'  # choose a color
    )
])
# Set layout
missing_values_bar_chart.update_layout(
    title='Number of Missing Values by Column',
    xaxis_title='Columns',
    yaxis_title='Missing Count'
)

# Create a boolean DataFrame where True indicates a missing value
missing_data = df.isnull()

# Convert the boolean values to integers
missing_data = missing_data.astype(int)

# Create a heatmap
missing_values_heatmap = go.Figure(data=go.Heatmap(
    z=missing_data.values,
    x=list(missing_data.columns),
    y=list(missing_data.index),
    colorscale=[[0, '#000000'], [1, '#FFFFFF']],
    showscale=False,
))

missing_values_heatmap.update_layout(
    title='Missing Values Heatmap',
    xaxis_title='Columns',
    yaxis_title='Rows',
)


"""This Code is for investigating and visualiseing the data types in the dataframe."""
#Create a stacked bar chart to show the differnet data types in each column of the dataframe.
investigate_dtype_df = investigate_dtype(df)
data_types = investigate_dtype_df.columns
#print(investigate_dtype_df)

# Define a color mapping for data types
data_types_color_mapping = {
    'int': 'blue',
    'float': 'orange',
    'str': 'purple',
    'datetime': 'yellow',
    'Timestamp': 'yellow',
    'char': 'teal',
    'other': 'brown',
    'NoneType':'grey',
    'zero' :'green' 
}

# Create a trace for each data type
data_types_traces = []
for dtype in data_types:
    data_types_traces.append(Bar(
        x=investigate_dtype_df.index,  # column names
        y=investigate_dtype_df[dtype],  # proportion of dtype in each column
        name=str(dtype),  # data type name
        marker_color=data_types_color_mapping.get(dtype, 'grey')  # use color mapping, default to 'grey' if dtype not in mapping
    ))

# Create the layout
data_types_layout = {
    'barmode': 'stack',
    'title': 'Data Types by Column'
}

# Create the figure
data_types_bar_chart = {
    'data': data_types_traces,
    'layout': data_types_layout
}

"""This Code is for investigating and visualiseing the unique values in the dataframe."""
# Unique values bar chart
unique_counts = count_unique_values(df).sort_values()

# Create a bar chart
unique_values_bar_chart = go.Figure(data=[
    go.Bar(
        x=unique_counts.index,  # column names
        y=unique_counts.values,  # unique counts
    )
])

# Set layout
unique_values_bar_chart.update_layout(
    title='Number of Unique Values by Column',
    xaxis_title='Columns',
    yaxis_title='Unique Count'
)

# Call the function to get the DataFrame of most common values
most_common_values_df = most_common_values(df, n=1)

# Create a title and a table for the most common values
most_common_values_table = html.Div([
    html.H3('Most Common Values'),
    dash_table.DataTable(
        id='most_common_values_table',
        columns=[{"name": i, "id": i} for i in most_common_values_df.columns],
        data=most_common_values_df.to_dict('records'),
    )
])


"""This code is for investigating the range of values in the dataframe and outliers."""
# Describe the dataframe
ranges = describe(df)

# Calculate outliers
outliers_counts = outliers(df)

# Convert to DataFrame and transpose
outliers_counts_df = pd.DataFrame(outliers_counts).T
print(outliers_counts_df)

ranges_outliers = pd.concat([ranges, outliers_counts_df])
#print(ranges_outliers)

# Add row labels as a column
ranges_outliers['Row'] = ranges_outliers.index

# Move the 'Row' column to the first position
ranges_outliers = ranges_outliers[ ['Row'] + [ col for col in ranges_outliers.columns if col != 'Row' ] ]


# Create a title and a table for the ranges
ranges_table = html.Div([
    html.H3('Ranges and Outliers'),
    dash_table.DataTable(
        id='ranges_table',
        columns=[{"name": i, "id": i} for i in ranges_outliers.columns],
        data=ranges_outliers.to_dict('records'),
    )
])


"""This Code is for setting up the layout of the dashboard."""
app.layout = html.Div(children=[
    html.H1(children='Data Profiling Dashboard'),
    characteristics_table,
    data_table, 
    dcc.Graph(id='missing_values_bar_chart', figure=missing_values_bar_chart),
    dcc.Graph(figure=missing_values_heatmap),
    dcc.Graph(id='graph', figure=data_types_bar_chart),
    dcc.Graph(id='unique_bar_chart', figure=unique_values_bar_chart),
    most_common_values_table,
    ranges_table
    ])