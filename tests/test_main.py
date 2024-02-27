
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import read_data
import pandas as pd

#test read data function
def test_read_data():
    # test reading a csv file
    assert read_data('test_data/imdb_top_1000.csv').equals(pd.read_csv('test_data/imdb_top_1000.csv'))
    # test reading an excel file
    assert read_data('test_data/bfi-weekend-box-office-report-2024-02-16-18.xlsx').equals(pd.read_excel('test_data/bfi-weekend-box-office-report-2024-02-16-18.xlsx'))
    # test reading a json file
    assert read_data('test_data/News_Category_Dataset_v3.json').equals(pd.read_json('test_data/News_Category_Dataset_v3.json', lines=True))
    # test reading an invalid file type
    assert read_data('data.txt') == 'Invalid file type'

test_read_data()