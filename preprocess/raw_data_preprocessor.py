from services.json_services import save_json_file
from .filter_tokenize_encode import *

def preprocess_raw_data(raw_data):
    preprocessed_data = tokenize_and_encode(raw_data)
    save_json_file(preprocessed_data, 'preprocessed_data_c2.json')
    
    return preprocessed_data