from preprocess import CLexer, CTokenEncoder
from services.json_services import *

# def find_bug_positions(
#     # lexer, encoder, 
#     literal_map_data,
#     buggy_src_code, accepted_raw_tokens, accepted_encoded_tokens
# ):
#     # Tokenize and encode buggy source code
#     # literal_map_data = read_json_file('literal_data_map.json')
#     lexer, encoder= CLexer(), CTokenEncoder(literal_map=literal_map_data)
    
#     buggy_raw_tokens = lexer.tokenize(buggy_src_code) # list of tuple (token_type, token_value)
#     buggy_raw_tokens_value = [token[1] for token in buggy_raw_tokens] # list of token_value
#     buggy_encoded_tokens = encoder.encode_tokens(buggy_raw_tokens) # list of encoded token

#     bug_positions = []
#     # Only consider the case where buggy data has the same number of tokens as the original data
#     if len(buggy_encoded_tokens) == len(accepted_encoded_tokens):
#         num_tokens = len(buggy_encoded_tokens)
#         for i in range(num_tokens):
#             # if the tokens of the two sequences are different -> bug
#             if buggy_encoded_tokens[i] != accepted_encoded_tokens[i]: 
#                 bug_positions.append({
#                     "token_location": i,
#                     "original_token": accepted_raw_tokens[i],
#                     "original_token_order": accepted_encoded_tokens[i],
#                     "error_token": buggy_raw_tokens_value[i]
#                 })
        
#         return (bug_positions, buggy_raw_tokens_value, buggy_encoded_tokens)

#     else:
#         return None
    
# def label_bug_positions(buggy_data, accepted_data):
#     accepted_data_dict = { src['judge_id']: src for src in accepted_data }
    
#     processed_buggy_data = []
    
#     for buggy_src in buggy_data:
#         judge_id = buggy_src.get('judge_id')
        
#         if judge_id in accepted_data_dict:
#             accepted_src = accepted_data_dict.get(judge_id)
            
#             buggy_src_code = buggy_src.get('source_code')
#             accepted_raw_tokens = accepted_src.get('raw_tokens')
#             accepted_encoded_tokens = accepted_src.get('encoded_tokens')
            
#             result = find_bug_positions(
#                 # lexer,
#                 # encoder, 
#                 buggy_src_code, accepted_raw_tokens, accepted_encoded_tokens
#             )
#             if result:
#                 bug_positions, buggy_raw_tokens, buggy_encoded_tokens = result
#                 print(f'judge_id {judge_id}: VALID! Appending into processed data...')
#                 processed_buggy_data.append({
#                     "judge_id": judge_id,
#                     "source_code": buggy_src_code,
#                     "raw_tokens": buggy_raw_tokens,
#                     "encoded_tokens": buggy_encoded_tokens,
#                     "bug_positions": bug_positions
#                 })
#             else:
#                 print(f'judge_id {judge_id}: INVALID')
    
#     if len(processed_buggy_data) > 0:
#         # 
#         # save_json_file(
#         #     data=encoder.get_literal_map(), 
#         #     file_name='literal_map_after_seeding.json'
#         #     )
#         # 
#         print('Done')
#         return processed_buggy_data
    
#     else:
#         print('Something went wrong')
#         return []

# New
def label_bug_positions(buggy_data, metrics_data):
    # Tạo dictionary để tra cứu nhanh object theo judge_id từ metrics_data
    metrics_dict = {obj["judge_id"]: obj for obj in metrics_data}

    labeled_buggy_data = []
    
    for buggy_obj in buggy_data:
        judge_id = buggy_obj["judge_id"]

        # Kiểm tra nếu judge_id tồn tại trong metrics_data
        if judge_id in metrics_dict:
            metrics_obj = metrics_dict[judge_id]

            # So sánh raw_tokens và encoded_tokens nếu chúng có cùng độ dài
            if (
                len(buggy_obj["raw_tokens"]) == len(metrics_obj["raw_tokens"])
                and len(buggy_obj["encoded_tokens"]) == len(metrics_obj["encoded_tokens"])
            ):
                bug_positions = []

                # So sánh raw_tokens
                for i, (buggy_token, metrics_token) in enumerate(zip(buggy_obj["raw_tokens"], metrics_obj["raw_tokens"])):
                    if buggy_token != metrics_token:
                        bug_positions.append({
                            "token_location": i,
                            "original_raw_token": metrics_token,
                            "error_raw_token": buggy_token,
                            "original_encoded_token": metrics_obj["encoded_tokens"][i],
                            "error_encoded_token": buggy_obj["encoded_tokens"][i]
                        })

                if len(bug_positions) > 0:
                    buggy_obj["bug_positions"] = bug_positions
                    labeled_buggy_data.append(buggy_obj)
    
    return labeled_buggy_data