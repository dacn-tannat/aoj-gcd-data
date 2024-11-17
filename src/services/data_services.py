from crawl import *
from preprocess import *
from seed import *

def process_prepare_data(file_name=None):
    # If data already exists, just read them. Else, crawl data from scratch
    if file_name:
        raw_data = read_json_file(file_name)
    else:
        raw_data = get_raw_data()
    
    # Pre-process raw data
    preprocessed_data = preprocess_raw_data(raw_data)

    return preprocessed_data

def process_split_data(file_name=None, split_ratio=0.9):
    # Read data
    if file_name:
        data = read_json_file(file_name)
    else:
        data = read_json_file('preprocessed_data.json')
        
    # Split from AC data into train_data (3882) and raw_metrics_data (432)
    train_data, raw_metrics_data = split_data(data=data, split_ratio=split_ratio)
    
    return train_data, raw_metrics_data
    
def process_generate_buggy_data(file_name=None):
    # Read data
    if file_name:
        data = read_json_file(file_name)
    else:
        data = read_json_file('raw_metrics_data.json')
    
    # Generate buggy data by sending prompt to LLM
    raw_buggy_data = generate_buggy_data(data)
    
    save_json_file(data=raw_buggy_data, file_name='raw_buggy_data.json')
    
    return raw_buggy_data

def process_filter_valid_buggy_data(file_name=None):
    if file_name:
        buggy_data = read_json_file(file_name)
    else:
        buggy_data = read_json_file('raw_buggy_data.json')
    
    # Submit each buggy source code to AOJ
    # Validate base on their submission status response from AOJ
    # Filter valid sources
    filtered_buggy_data = validate_and_filter_valid_buggy_data(buggy_data)
    
    save_json_file(data=filtered_buggy_data, file_name='filtered_buggy_data.json')
    
    return filtered_buggy_data

def process_label_bug_positions():
    buggy_data = read_json_file('filtered_buggy_data.json')
    accepted_data = read_json_file('preprocessed_data.json')
    
    processed_buggy_data = label_bug_positions(buggy_data, accepted_data)
    
    save_json_file(data=processed_buggy_data, file_name='processed_buggy_data.json')
    
    return processed_buggy_data

def process_merge_data():
    raw_metrics_data = read_json_file('raw_metrics_data.json')
    processed_buggy_data = read_json_file('processed_buggy_data.json')
    
    merged_data = merge_data(raw_metrics_data, processed_buggy_data, shuffle=True)
    
    save_json_file(data=merged_data, file_name='processed_metrics_data.json')
    
    return merged_data

def process_label_line_for_bug():
    processed_metrics_data = read_json_file('processed_metrics_data.json')
    
    line_processed_metrics_data = label_line_for_bug(data=processed_metrics_data)
    
    save_json_file(data=line_processed_metrics_data, file_name='line_processed_metrics_data.json')
    
    return line_processed_metrics_data