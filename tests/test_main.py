# We will write our test cases in this file
from backend.data_processing import read_data, missing_data, dtype, duplicate_data
import pandas as pd

test_csv = "data/imdb_top_1000.csv"
test_excel = "data/bfi-weekend-box-office-report-2024-02-16-18.xlsx"
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

# tests missing data function
def test_missing_data():
    # reads in the data
    df_csv = read_data(test_csv)
    df_excel = read_data(test_excel)
    df_json = read_data(test_json)
    # tests on a csv file
    assert missing_data(df_csv).equals(df_csv.isna().sum())
    #print(missing_data(df_csv))
    # tests on a excel file
    assert missing_data(df_excel).equals(df_excel.isna().sum())
    #print(missing_data(df_excel))
    # tests on a json file
    assert missing_data(df_json).equals(df_json.isna().sum())
    #print(missing_data(df_json))

# tests dtype function
def test_dtype():
    # reads in the data
    df_csv = read_data(test_csv)
    df_excel = read_data(test_excel)
    df_json = read_data(test_json)
    # tests on a csv file
    assert dtype(df_csv).equals(df_csv.dtypes)
    #print(dtype(df_csv))
    # tests on a excel file
    assert dtype(df_excel).equals(df_excel.dtypes)
    #print(dtype(df_excel))
    # tests on a json file
    assert dtype(df_json).equals(df_json.dtypes)
    #print(dtype(df_json))

# tests duplicate data function
def test_duplicate_data():
    # reads in the data
    df_csv = read_data(test_csv)
    df_excel = read_data(test_excel)
    df_json = read_data(test_json)
    # tests on a csv file
    assert duplicate_data(df_csv) == df_csv.duplicated().sum()
    #print(duplicate_data(df_csv))
    # tests on a excel file
    assert duplicate_data(df_excel) == df_excel.duplicated().sum()
    #print(duplicate_data(df_excel))
    # tests on a json file
    assert duplicate_data(df_json) == df_json.duplicated().sum()
    #print(duplicate_data(df_json))