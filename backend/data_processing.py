import pandas as pd
import numpy as np


#Function checks the type of file and then reads the data into a pandas dataframe the acceptable 
# file types are csv, excel, and json
def read_data(file_path):
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        return pd.read_excel(file_path)
    elif file_path.endswith('.json'):
        return pd.read_json(file_path, lines=True)
    else:
        return 'Invalid file type'


# Function checks for missing data in a dataframe
def count_missing_data(df):
    # check for missing data
    missing = df.isna().sum()
    return missing

# Function checks for data types in a dataframe
def dtype(df):
    # check for data types
    dtypes = df.dtypes
    return dtypes

# Function checks for duplicate data in a dataframe
def count_duplicate_data(df):
    # check for duplicate data
    duplicate = df.duplicated().sum()
    return duplicate

def count_unique_values(df):
    # check for unique values
    unique = df.nunique()
    return unique

# Function checks for the correlation between columns in a dataframe
def correlation(df):
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    corr = numeric_df.corr()
    return corr