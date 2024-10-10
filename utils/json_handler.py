import json
from collections import defaultdict
from functools import reduce

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def count_status_objects(data):
    status_count = defaultdict(int)  

    for obj in data:
        status = obj.get('status', None)  
        if status is not None:
            status_count[status] += 1

    return dict(status_count)

def calculate_average_tokens(data, file_path, status=None):
    data = read_json_file(file_path)
    filtered_data = [obj for obj in data if status is None or obj['status'] == status]
    
    if not filtered_data:
        return 0
    
    total_tokens = sum(len(obj.get('raw_tokens')) for obj in filtered_data)
    average_tokens = total_tokens / len(filtered_data)

    return average_tokens

def save_json_file(data, file_path):
    formatted_json = json.dumps(data, separators=(',', ':'))
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(formatted_json)
