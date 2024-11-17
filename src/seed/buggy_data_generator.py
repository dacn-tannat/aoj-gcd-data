from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()

api_keys = [
    os.getenv('GROQ_LLAMA_3.1_70B_API_KEY_1'),
    os.getenv('GROQ_LLAMA_3.1_70B_API_KEY_2'),
    os.getenv('GROQ_LLAMA_3.1_70B_API_KEY_3'),
    os.getenv('GROQ_LLAMA_3.1_70B_API_KEY_4'),
    os.getenv('GROQ_LLAMA_3.1_70B_API_KEY_5'),
    os.getenv('GROQ_LLAMA_3.1_70B_API_KEY_6'),
    os.getenv('GROQ_LLAMA_3.1_70B_API_KEY_7'),
    os.getenv('GROQ_LLAMA_3.1_70B_API_KEY_8'),
    os.getenv('GROQ_LLAMA_3.1_70B_API_KEY_9'),
    os.getenv('GROQ_LLAMA_3.1_70B_API_KEY_10'),
    os.getenv('GROQ_LLAMA_3.1_70B_API_KEY_11'),
    os.getenv('GROQ_LLAMA_3.1_70B_API_KEY_12')
]

def prompt(data):
    prompt = f"""
The following object contains accurate source code for a GCD (Greatest Common Divisor) problem: 
{data}
Your task is to modify the input source code, return 5 modified source codes while ensuring that:
    1. The modified returned source codes must still compile and do not have runtime error or infinity loop, but return incorrect results.
    2. Each modified returned source codes must be changed in distinct and intentional token.
    3. Keep ALL the end line tokens "\\n" in source code (but NOT in JSON object).
    3. Keep the response minimal, with no extra explanations beyond the required data.
Return the JSON object with exactly 2 key-value pairs: "judge_id" and an array "source_codes", with each element in "source_codes" is a string of source code contained bugs as requested

Important Notes:
    1. Replace the original token only, without adding or removing any other tokens.
    2. Ensure return the VALID JSON object only, without any other contents, raw_tokens, encoded_tokens or additional explanation.
"""
    return prompt

def prompt_llm_to_seed_bug(data):
    for i, api_key in enumerate(api_keys, start=1):
        try:
            client = Groq(api_key=api_key)
            chat_completion = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[{
                    "role": "user",
                    "content": prompt(data),
                }],
                response_format={
                    "type": "json_object",
                }
            )
            response = chat_completion.choices[0].message.content
            
            print(f'Using GROQ_LLAMA_3.1_70B_API_KEY_{i} successfully!')
            return response
        except Exception as e:
            print(f'Error occurred with GROQ_LLAMA_3.1_70B_API_KEY_{i}: {e}\nTrying next API Key...')
            continue  # Try next API Key if current one fails
        
    # If all API keys failed
    print("All API keys exhausted without success.")
    return None

def generate_buggy_data(data):
    raw_buggy_data = []
    count = 1
    max_buggy_objects = 0.5 * len(data)
        
    for src in data:
        result = prompt_llm_to_seed_bug(src)
        if result is not None:
            raw_buggy_data.append(json.loads(result))
            print(f'{count} - {src["judge_id"]}')
            count += 1
        else:
            print("Terminating as all API keys failed.")
            break  # Break if all API keys have been tried without success
            
        if count > max_buggy_objects:
            break
    
    # Save the accumulated data to JSON regardless of success/failure
    return raw_buggy_data