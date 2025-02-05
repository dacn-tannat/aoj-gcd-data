import json
import os

def read_json_file(file_name):
    # Get the data directory path
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
    
    # Create the full file path
    file_path = os.path.join(data_dir, file_name)
    
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def save_json_file(data, file_name):
    # Ensure the data directory exists
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Create the full file path
    file_path = os.path.join(data_dir, file_name)
    
    formatted_json = json.dumps(data, separators=(',', ':'))
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(formatted_json)

def analyze_json_data(json_data):
    total_objects = len(json_data)  # Tổng số đối tượng
    status_count = {}  # Đếm số lượng object từng loại dựa trên status
    total_tokens = 0  # Tổng số tokens
    count_status_4 = 0  # Số lượng object có status = 4
    total_tokens_status_4 = 0  # Tổng số tokens của object có status = 4

    for obj in json_data:
        # Tính số lượng object theo status
        status = obj.get("status")
        if status in status_count:
            status_count[status] += 1
        else:
            status_count[status] = 1
        
        # Tính tổng số tokens
        num_tokens = len(obj.get("raw_tokens", []))
        total_tokens += num_tokens
        
        # Tính tổng số tokens của object có status = 4
        if status == 4:
            count_status_4 += 1
            total_tokens_status_4 += num_tokens

    # Tính số token trung bình
    average_tokens = total_tokens / total_objects if total_objects > 0 else 0
    average_tokens_status_4 = total_tokens_status_4 / count_status_4 if count_status_4 > 0 else 0

    # Kết quả thống kê
    statistics = {
        "total_objects": total_objects,
        "status_count": status_count,
        "average_tokens": average_tokens,
        "average_tokens_status_4": average_tokens_status_4
    }

    print(f"Total Objects: {statistics['total_objects']}")
    print("Status Count:")
    for status, count in statistics['status_count'].items():
        print(f"  Status {status}: {count}")
    print(f"Average Tokens: {statistics['average_tokens']:.2f}")
    print(f"Average Tokens (Status = 4): {statistics['average_tokens_status_4']:.2f}")