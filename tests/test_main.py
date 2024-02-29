# We will write our test cases in this file
from backend.data_processing import read_data, count_missing_data, check_dtype, count_duplicate_data, count_unique_values, correlation, investigate_dtype
import pytest
import pandas as pd

test_csv = "data/imdb_top_1000.csv"
test_excel = "data/1617fedschoolcodelist.xls"
test_json = "data/News_Category_Dataset_v3.json"

# tests read data function
def test_read_data():
    # test reading a csv file
    assert read_data(test_csv).equals(pd.read_csv(test_csv))
    # test reading an excel file
    assert read_data(test_excel).equals(pd.read_excel(test_excel))
    # test reading a json file
    assert read_data(test_json).equals(pd.read_json(test_json, lines=True))
    # test reading an invalid file type
    assert read_data('data.txt') == 'Invalid file type'

# tests count missing data function
def test_count_missing_data():
    # reads in the data
    df_csv = read_data(test_csv)
    df_excel = read_data(test_excel)
    df_json = read_data(test_json)
    # tests on a csv file
    assert count_missing_data(df_csv).equals(df_csv.isna().sum())
    #print(missing_data(df_csv))
    # tests on a excel file
    assert count_missing_data(df_excel).equals(df_excel.isna().sum())
    #print(missing_data(df_excel))
    # tests on a json file
    assert count_missing_data(df_json).equals(df_json.isna().sum())
    #print(missing_data(df_json))

# tests dtype function
def test_check_dtype():
    # reads in the data
    df_csv = read_data(test_csv)
    df_excel = read_data(test_excel)
    df_json = read_data(test_json)
    # tests on a csv file
    assert check_dtype(df_csv).equals(df_csv.dtypes)
    #print(dtype(df_csv))
    # tests on a excel file
    assert check_dtype(df_excel).equals(df_excel.dtypes)
    #print(dtype(df_excel))
    # tests on a json file
    assert check_dtype(df_json).equals(df_json.dtypes)
    #print(dtype(df_json))


# Testing for investigate_dtype function
data = {'col1': ['string1', 'string2', 1, 2.5],
        'col2': [1.0, 2.0, None, 'string']}
df = pd.DataFrame(data)
@pytest.mark.parametrize('col_name, expected_counts', [
    ('col1', {'str': 0.5, 'int': 0.25, 'float': 0.25}),
    ('col2', {'float': 0.5, 'NoneType': 0.25, 'str': 0.25})
])
def test_investigate_dtype(col_name, expected_counts):
    # Create a smaller DataFrame with the specified column for testing
    test_df = df[[col_name]]

    # Call the function and get the result
    result_df = investigate_dtype(test_df)

    # Get the data type counts for the specific column
    actual_counts = result_df.iloc[0].to_dict()

    # Assert that the actual and expected counts are equal
    assert actual_counts == expected_counts, f"Counts for {col_name} are not as expected: {actual_counts} != {expected_counts}"


# tests count duplicate data function
def test_count_duplicate_data():
    # reads in the data
    df_csv = read_data(test_csv)
    df_excel = read_data(test_excel)
    df_json = read_data(test_json)
    # tests on a csv file
    assert count_duplicate_data(df_csv) == df_csv.duplicated().sum()
    #print(duplicate_data(df_csv))
    # tests on a excel file
    assert count_duplicate_data(df_excel) == df_excel.duplicated().sum()
    #print(duplicate_data(df_excel))
    # tests on a json file
    assert count_duplicate_data(df_json) == df_json.duplicated().sum()
    #print(duplicate_data(df_json))

# tests count unique values function
def test_count_unique_values():
    # reads in the data
    df_csv = read_data(test_csv)
    df_excel = read_data(test_excel)
    df_json = read_data(test_json)
    # tests on a csv file
    assert count_unique_values(df_csv).equals(df_csv.nunique())
    #print(unique_values(df_csv))
    # tests on a excel file
    assert count_unique_values(df_excel).equals(df_excel.nunique())
    #print(unique_values(df_excel))
    # tests on a json file
    assert count_unique_values(df_json).equals(df_json.nunique())
    #print(unique_values(df_json))

# tests correlation function
def test_correlation():
    # reads in the data
    df_csv = read_data(test_csv).select_dtypes(include=['float64', 'int64'])
    df_excel = read_data(test_excel).select_dtypes(include=['float64', 'int64'])
    df_json = read_data(test_json).select_dtypes(include=['float64', 'int64'])
    # tests on a csv file
    assert correlation(df_csv).equals(df_csv.corr())
    #print(correlation(df_csv))
    # tests on a excel file
    assert correlation(df_excel).equals(df_excel.corr())
    #print(correlation(df_excel))
    # tests on a json file
    assert correlation(df_json).equals(df_json.corr())
    #print(correlation(df_json))