"""
Main script for processing raw data.

This script imports necessary functions from the services module and processes
the raw data stored in 'raw_data_c.json' when run as the main program.
"""

from services import process_data
from preprocess import filter_accepted_codes

if __name__ == '__main__':
    '''
    Usage:
    1. Crawl and pre-process data: 
        process_data()
    2. Just pre-process existed raw data: 
        process_data('raw_data_c.json')
        
    3. Filter accepted codes:
        accepted_codes = filter_accepted_codes('raw_data_c.json')
        accepted_codes = filter_accepted_codes('preprocessed_data_c.json')
    '''
    process_data()
    # accepted_codes = filter_accepted_codes('preprocessed_data_c.json')


# import os
# import requests
# import json
# from services import read_json_file
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()
# GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'
# headers = {
#     'Content-Type': 'application/json',
# }

# data = read_json_file('accepted_preprocessed_data_c.json')

# if not data:
#     print("No data found in accepted_preprocessed_data_c.json.")
# else:
#     prompt_text = f"This object contains information about the correct source code for a GCD (Greatest Common Divisor) problem. Here is the object data:\n{data[0]}\nPlease inject 3-4 logical bugs into the source code so that it still compiles, but returns incorrect results. Finally, return the object containing the faulty source code with the following template:\n{{\n  \"judge_id\": <judge_id>,\n  \"source_code\": \"<source_code>\",\n  \"status\": <status>,\n  \"raw_tokens\": <raw_tokens>,\n  \"bug_positions\": [\n    {{\n      \"line\": <line>,\n      \"token_location\": <token_location>,\n      \"original_token\": \"<original_token>\",\n      \"error_token\": \"<error_token>\"\n    }}\n  ]\n}}"

#     payload = {
#         "contents": [
#             {
#                 "parts": [
#                     {
#                         "text": prompt_text
#                     }
#                 ]
#             }
#         ]
#     }

#     try:
#         response = requests.post(url, headers=headers, params={'key': GEMINI_API_KEY}, json=payload)

#         if response.status_code == 200:
#             response_data = response.json()
#             candidate = response_data['candidates'][0]['content']['parts'][0]['text']
            
#             print(candidate)
#             # if 'candidates' in response_data and len(response_data['candidates']) > 0:
#             #     candidate = response_data['candidates'][0]
#             #     judge_id = candidate['content']['parts'][0]['text'].split('\"judge_id\": ')[1].split(',')[0]
#             #     source_code = candidate['content']['parts'][0]['text'].split('\"source_code\": \"')[1].split('\"')[0]
#             #     status = candidate['content']['parts'][0]['text'].split('\"status\": ')[1].split(',')[0]
#             #     raw_tokens = json.loads(candidate['content']['parts'][0]['text'].split('\"raw_tokens\": ')[1].split(']')[0] + ']')
#             #     bug_positions_text = candidate['content']['parts'][0]['text'].split('\"bug_positions\": ')[1].split(']')[0] + ']'
#             #     bug_positions = json.loads(bug_positions_text)

#             #     print(f"Judge ID: {judge_id}")
#             #     print(f"Source Code:\n{source_code}")
#             #     print(f"Status: {status}")
#             #     print(f"Raw Tokens: {raw_tokens}")
#             #     print(f"Bug Positions: {bug_positions}")
#             # else:
#             #     print("No candidates found in the response.")
#         else:
#             print(f"Error: {response.status_code}, {response.text}")

#     except Exception as e:
#         print(f"An error occurred: {e}")