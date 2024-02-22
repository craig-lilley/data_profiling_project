import pandas as pd
import numpy as np


# create a function that checks the type of file and then reads the data into a pandas dataframe the acceptable 
# file types should be csv, excel, and json
def read_data(file_path):
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        return pd.read_excel(file_path)
    elif file_path.endswith('.json'):
        return pd.read_json(file_path)
    else:
        return 'Invalid file type'