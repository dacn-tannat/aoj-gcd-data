from services.json_services import read_json_file, save_json_file

def filter_accepted_codes():
    data = read_json_file('preprocessed_data_c.json')
    accepted_codes = [src for src in data if src['status'] == 4]
    
    save_json_file(accepted_codes, 'accepted_codes_c.json')
    
    return accepted_codes