# We will write our test cases in this file
from backend.data_processing import read_data, missing_data, dtype, duplicate_data
import pandas as pd

# tests read data function
def test_read_data():
    # test reading a csv file
    assert read_data('data/imdb_top_1000.csv').equals(pd.read_csv('data/imdb_top_1000.csv'))
    # test reading an excel file
    assert read_data('data/bfi-weekend-box-office-report-2024-02-16-18.xlsx').equals(pd.read_excel('data/bfi-weekend-box-office-report-2024-02-16-18.xlsx'))
    # test reading a json file
    assert read_data('data/News_Category_Dataset_v3.json').equals(pd.read_json('data/News_Category_Dataset_v3.json', lines=True))
    # test reading an invalid file type
    assert read_data('data.txt') == 'Invalid file type'

# tests missing data function
def test_missing_data():
    # reads in the data
    df_csv = read_data('data/imdb_top_1000.csv')
    df_excel = read_data('data/bfi-weekend-box-office-report-2024-02-16-18.xlsx')
    df_json = read_data('data/News_Category_Dataset_v3.json')
    # tests on a csv file
    assert missing_data(df_csv).equals(df_csv.isna().sum())
    # tests on a excel file
    assert missing_data(df_excel).equals(df_excel.isna().sum())
    # tests on a json file
    assert missing_data(df_json).equals(df_json.isna().sum())

# tests dtype function
def test_dtype():
    # reads in the data
    df_csv = read_data('data/imdb_top_1000.csv')
    df_excel = read_data('data/bfi-weekend-box-office-report-2024-02-16-18.xlsx')
    df_json = read_data('data/News_Category_Dataset_v3.json')
    # tests on a csv file
    assert dtype(df_csv).equals(df_csv.dtypes)
    # tests on a excel file
    assert dtype(df_excel).equals(df_excel.dtypes)
    # tests on a json file
    assert dtype(df_json).equals(df_json.dtypes)

# tests duplicate data function
def test_duplicate_data():
    # reads in the data
    df_csv = read_data('data/imdb_top_1000.csv')
    df_excel = read_data('data/bfi-weekend-box-office-report-2024-02-16-18.xlsx')
    df_json = read_data('data/News_Category_Dataset_v3.json')
    # tests on a csv file
    assert duplicate_data(df_csv) == df_csv.duplicated().sum()
    # tests on a excel file
    assert duplicate_data(df_excel) == df_excel.duplicated().sum()
    # tests on a json file
    assert duplicate_data(df_json) == df_json.duplicated().sum()