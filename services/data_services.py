from crawl.raw_data_handler import get_raw_data
from preprocess.raw_data_preprocessor import preprocess_raw_data
from services.json_services import read_json_file

def process_data(file_path=None):
    if file_path:
        raw_data = read_json_file(file_path)
    else:
        raw_data = get_raw_data()
    
    preprocessed_data = preprocess_raw_data(raw_data)
    
    return preprocessed_data