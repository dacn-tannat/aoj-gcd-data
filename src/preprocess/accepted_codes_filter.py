from services.json_services import read_json_file, save_json_file

def filter_accepted_codes(file_name):
    data = read_json_file(file_name=file_name)
    accepted_codes = [src for src in data if src['status'] == 4]
    
    save_json_file(data=accepted_codes, file_name='accepted_codes_c.json')
    
    return accepted_codes