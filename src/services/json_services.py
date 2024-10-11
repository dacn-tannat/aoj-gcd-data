import json
import os

def read_json_file(file_name):
    # Get the data directory path
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
    
    # Create the full file path
    file_path = os.path.join(data_dir, file_name)
    
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def save_json_file(data, file_name):
    # Ensure the data directory exists
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Create the full file path
    file_path = os.path.join(data_dir, file_name)
    
    formatted_json = json.dumps(data, separators=(',', ':'))
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(formatted_json)
