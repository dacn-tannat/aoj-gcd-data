from preprocess import CLexer, CTokenEncoder
from services.json_services import *

def get_bug_positions(err_source_code, ac_raw_tokens, ac_encoded_tokens):
    literal_map_data = read_json_file('literal_map_data.json')
    lexer, encoder = CLexer(), CTokenEncoder(literal_map_data)
    
    err_raw_tokens = lexer.tokenize(err_source_code)
    err_raw_tokens_value = [token[1] for token in err_raw_tokens]
    err_encoded_tokens = encoder.encode_tokens(err_raw_tokens)
        
    bug_positions = []
    if len(err_encoded_tokens) == len(ac_encoded_tokens):
        for i in range(len(err_encoded_tokens)):
            if err_encoded_tokens[i] != ac_encoded_tokens[i]:
                bug_positions.append({
                    "token_location": i,
                    "original_token": ac_raw_tokens[i],
                    "original_token_order": ac_encoded_tokens[i],
                    "error_token": err_raw_tokens_value[i]
                })
        return bug_positions, err_raw_tokens_value, err_encoded_tokens
    else:
        return None, None, None
    
def process_labeling_bug_positions():
    err_data = read_json_file('erroneous_processed_data_c.json')
    ac_data = read_json_file('accepted_preprocessed_data_c.json')
    
    ac_data_dict = {src['judge_id']: src for src in ac_data}
    
    processed_data = []
    
    for err_item in err_data:
        judge_id = err_item.get('judge_id')
        print(f'Finding judge_id {judge_id}...')
        
        if judge_id in ac_data_dict:
            ac_item = ac_data_dict.get(judge_id)
            print(f'Found judge_id {judge_id}!')
            
            total_err_source_codes = len(err_item.get('source_codes'))
            for index, err_source_code in enumerate(err_item.get('source_codes')):
                print(f'Processing source code {index + 1}/{total_err_source_codes}...')
                bug_positions, err_raw_tokens, err_encoded_tokens = get_bug_positions(err_source_code, ac_item.get('raw_tokens'), ac_item.get('encoded_tokens'))
                if bug_positions and err_raw_tokens and err_encoded_tokens:
                    print('Valid error! Appending into processed data...')
                    processed_data.append({
                        "judge_id": judge_id,
                        "source_code": err_source_code,
                        "raw_tokens": err_raw_tokens,
                        "encoded_tokens": err_encoded_tokens,
                        "bug_positions": bug_positions
                    })
                else:
                    print('Invalid errors!')
    
    if len(processed_data) > 0:
        save_json_file(processed_data, 'buggy_data_with_label.json')
        print('Data saved successfully')
        return processed_data
    
    else:
        print('Something went wrong')
        return None
    