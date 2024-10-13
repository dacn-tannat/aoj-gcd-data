import os
import time
import json
import requests
from dotenv import load_dotenv

# Load variable from .env
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# API URL of model
API_URL = "https://api.google.com/gemini/v1.5/generate"

def call_gemini_api(object_data, headers):
    prompt = f"Seed lỗi cho object sau: {object_data}"
    payload = {
        "model": "Gemini 1.5 Pro",
        "prompt": prompt,
        "max_tokens": 500
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Hàm gửi các request theo nhóm, với giới hạn 60 requests/phút
def send_requests_with_rate_limit(objects, headers, batch_size=60, wait_time=60):
    results = []
    total_objects = len(objects)

    for i in range(0, total_objects, batch_size):
        batch = objects[i:i + batch_size]

        for obj in batch:
            result = call_gemini_api(obj, headers)
            if result:
                results.append(result)

        print(f"Đã gửi {i + len(batch)} request, chờ {wait_time} giây trước khi tiếp tục...")
        time.sleep(wait_time)

    return results

def main():
    input_file = 'accepted_preprocessed_data_c.json'
    output_file = 'error_data.json'

    with open(input_file, 'r') as f:
        objects = json.load(f)

    headers = {
        'Authorization': f'Bearer {GEMINI_API_KEY}',
        'Content-Type': 'application/json'
    }

    results = send_requests_with_rate_limit(objects, headers)

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)

    print(f"Kết quả đã được lưu vào {output_file}")

if __name__ == '__main__':
    main()
