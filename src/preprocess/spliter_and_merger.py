from services.json_services import *

def split_data(data, split_ratio=0.9):
    split_index = int(split_ratio * len(data))
    train_data = data[:split_index]
    raw_metrics_data = data[split_index:]
    
    save_json_file(data=train_data, file_name='train_data.json')
    save_json_file(data=raw_metrics_data, file_name='raw_metrics_data.json')
    
    return train_data, raw_metrics_data

def merge_data(raw_data, processed_data, shuffle=False):
    # Bước 2: Tạo tập hợp các `judge_id` đã có trong processed_data
    processed_judge_ids = {obj['judge_id'] for obj in processed_data}
    
    # Bước 3: Lọc các object trong raw_data không có trong processed_data và thêm trường bug_positions = []
    filtered_data = [
        {**obj, 'bug_positions': []}
        for obj in raw_data if obj['judge_id'] not in processed_judge_ids
    ]
    
    # Bước 4: Gộp các object đã xử lý vào processed_data
    merged_data = processed_data + filtered_data
    
    # Bước 5: Trộn dữ liệu
    if shuffle:
        import random
        random.shuffle(merged_data)
    
    # Bước 6: Ghi dữ liệu đã gộp vào file mới
    return merged_data
    
    