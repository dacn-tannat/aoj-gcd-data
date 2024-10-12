from services.json_services import save_json_file
from .tokenize_encode_filter import *

def preprocess_raw_data(raw_data):
    """
    Preprocess the raw data by tokenizing, encoding, and filtering.

    Args:
        raw_data (list): A list of dictionaries containing raw source code data.

    Returns:
        list: A list of preprocessed data dictionaries, including tokenized and encoded information.

    This function performs the following steps:
    1. Calls tokenize_and_encode() to tokenize and encode the raw source code data.
    2. Saves the preprocessed data to a JSON file named 'preprocessed_data_c2.json'.
    3. Returns the preprocessed data.

    Note:
        The preprocessed data is saved to disk, allowing for easy retrieval in future processing steps.
    """
    preprocessed_data = tokenize_and_encode(raw_data)
    save_json_file(preprocessed_data, 'preprocessed_data_c2.json')
    
    return preprocessed_data
