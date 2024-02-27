# We will write our test cases in this file
from backend.data_processing import read_data
import pandas as pd

#test read data function
def test_read_data():
    # test reading a csv file
    assert read_data('data/imdb_top_1000.csv').equals(pd.read_csv('data/imdb_top_1000.csv'))
    # test reading an excel file
    assert read_data('data/bfi-weekend-box-office-report-2024-02-16-18.xlsx').equals(pd.read_excel('data/bfi-weekend-box-office-report-2024-02-16-18.xlsx'))
    # test reading a json file
    assert read_data('data/News_Category_Dataset_v3.json').equals(pd.read_json('data/News_Category_Dataset_v3.json', lines=True))
    # test reading an invalid file type
    assert read_data('data.txt') == 'Invalid file type'

test_read_data()