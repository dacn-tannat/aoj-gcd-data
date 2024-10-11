import json

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def save_json_file(data, file_path):
    formatted_json = json.dumps(data, separators=(',', ':'))
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(formatted_json)
