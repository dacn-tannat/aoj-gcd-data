"""
Main script for processing raw data.

This script imports necessary functions from the services module and processes
the raw data stored in 'raw_data_c.json' when run as the main program.
"""

from services import process_data
from preprocess import filter_accepted_codes
from seed import *

if __name__ == '__main__':
    '''
    Usage:
    1. Crawl and pre-process data: 
        process_data()
    2. Just pre-process existed raw data: 
        process_data('raw_data_c.json')
    3. Filter accepted codes:
        accepted_codes = filter_accepted_codes('raw_data_c.json')
        accepted_codes = filter_accepted_codes('preprocessed_data_c.json')
    '''
    submit_code_and_validate()
    