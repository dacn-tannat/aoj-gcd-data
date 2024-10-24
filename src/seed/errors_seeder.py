from groq import Groq
import json
from services import read_json_file, save_json_file
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv('LLAMA_API_KEY'),
)
    
def generate_erroneous_code(data):
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""The following object contains accurate source code for a GCD (Greatest Common Divisor) problem: 
                {data}
            Your task is to modify the input source code, return 5 modified source codes while ensuring that:
                1. The modified returned source codes must still compile and do not have runtime error or infinity loop, but return incorrect results.
                2. Each modified returned source codes must be changed in distinct and intentional token.
                3. Keep ALL the end line tokens "\\n" in source code (but NOT in JSON object).
                3. Keep the response minimal, with no extra explanations beyond the required data.
            Return the JSON object with some key-value pairs like "judge_id" and an array "source_codes".
                
            Important Notes:
                1. Replace the original token only, without adding or removing any other tokens.
                2. Ensure return the VALID JSON object only, without any other contents, raw_tokens, encoded_tokens or additional explanation.

            """,
                }
            ],
            model="llama-3.1-70b-versatile",
            response_format={
                "type": "json_object",
                }
        )
    
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def process_generate_erroneous_data():
    
    data = read_json_file('accepted_preprocessed_data_c.json')
        
    results = []
    count = 1

    # result = generate_erroneous_code(data[0])
    # y = json.loads(result)
    # results.append(y)
    for json_object in data:
        result = generate_erroneous_code(json_object)
        if result is not None:
            results.append(json.loads(result))
            print(count)
            count += 1
        if count > 100:
            break
            
    save_json_file(results, 'erroneous_raw_data_c.json')