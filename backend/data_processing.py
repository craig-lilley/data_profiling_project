import pandas as pd
import numpy as np


#Function checks the type of file and then reads the data into a pandas dataframe the acceptable 
# file types are csv, excel, and json
def read_data(file_path):
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        return pd.read_excel(file_path)
    elif file_path.endswith('.json'):
        return pd.read_json(file_path, lines=True)
    else:
        return 'Invalid file type'

#checks the type of file and returns the file type
def file_type(file_path):
    if file_path.endswith('.csv'):
        return 'CSV'
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        return 'Excel'
    elif file_path.endswith('.json'):
        return 'JSON'
    else:
        return 'Invalid file type'

# Function checks for missing data in a dataframe
def count_missing_data(df):
    # check for missing data
    missing = df.isna().sum()
    return missing

# Function checks changes dtype if obviousely wrong dataframe
def fix_numerical_dtype(df, threshold=0.9):
    for col in df.columns:
        # Try to convert the column to a numeric type
        df_numeric = pd.to_numeric(df[col], errors='coerce')

        # Check if a sufficient percentage of values were successfully converted
        if df_numeric.notnull().mean() > threshold:
            # Replace the original column with the converted column
            df[col] = df_numeric

    return df

def investigate_dtype(df):
    result = []

    for col in df.columns:
        types = df[col].map(lambda x: 'NaN' if pd.isna(x) else ('zero' if x == 0 else ('int' if isinstance(x, int) else ('float' if isinstance(x, float) else type(x).__name__))))
        type_counts = types.value_counts(normalize=True)
        type_counts_df = pd.DataFrame(type_counts).T
        type_counts_df.index = [col]
        result.append(type_counts_df)

    result_df = pd.concat(result)
    return result_df

# Function checks for duplicate data in a dataframe
def count_duplicate_data(df):
    # check for duplicate data
    duplicate = df.duplicated().sum()
    return duplicate

def count_unique_values(df):
    # check for unique values
    unique = df.nunique()
    return unique

def describe(df):
    data_desc = df.describe()
    return data_desc

def outliers(df):
    outliers = {}
    # Select only numeric columns
    df_numeric = df.select_dtypes(include=[np.number])
    
    # Calculate IQR
    Q1 = df_numeric.quantile(0.25)
    Q3 = df_numeric.quantile(0.75)
    IQR = Q3 - Q1
    
    # Define outliers
    low_outliers = (df_numeric < (Q1 - 1.5 * IQR))
    high_outliers = (df_numeric > (Q3 + 1.5 * IQR))
    
    
    # Count outliers
    outliers['Low Outliers'] = low_outliers.sum()
    outliers['High Outliers'] = high_outliers.sum()
    
    return outliers

# Function checks for the correlation between columns in a dataframe
def correlation(df):
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    corr = numeric_df.corr()
    return corr


