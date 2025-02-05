from crawl import *
from preprocess import *
from seed import *
from buggy_model import *
from math import ceil


def process_prepare_data(file_name=None):
    # If data already exists, just read them. Else, crawl data from scratch
    if file_name:
        raw_data = read_json_file(file_name)
    else:
        raw_data = get_raw_data()
    
    # Pre-process raw data
    preprocessed_data = preprocess_raw_data(raw_data)

    return preprocessed_data

def process_split_data(file_name=None, split_ratio=0.9):
    # Read data
    if file_name:
        data = read_json_file(file_name)
    else:
        data = read_json_file('preprocessed_data.json')
        
    # Split from AC data into train_data (3882) and raw_metrics_data (432)
    train_data, raw_metrics_data = split_data(data=data, split_ratio=split_ratio)
    
    return train_data, raw_metrics_data
    
def process_generate_buggy_data(file_name=None):
    # Read data
    if file_name:
        data = read_json_file(file_name)
    else:
        data = read_json_file('raw_metrics_data.json')
    
    # Generate buggy data by sending prompt to LLM
    raw_buggy_data = generate_buggy_data(data)
    
    save_json_file(data=raw_buggy_data, file_name='raw_buggy_data.json')
    
    return raw_buggy_data

def process_filter_valid_buggy_data(file_name=None):
    if file_name:
        buggy_data = read_json_file(file_name)
    else:
        buggy_data = read_json_file('raw_buggy_data.json')
    
    # Submit each buggy source code to AOJ
    # Validate base on their submission status response from AOJ
    # Filter valid sources
    filtered_buggy_data = validate_and_filter_valid_buggy_data(buggy_data)
    
    save_json_file(data=filtered_buggy_data, file_name='filtered_buggy_data.json')
    
    return filtered_buggy_data

# def process_label_bug_positions():
#     buggy_data = read_json_file('filtered_buggy_data.json')
#     accepted_data = read_json_file('preprocessed_data.json')
    
#     processed_buggy_data = label_bug_positions(buggy_data, accepted_data)
    
#     save_json_file(data=processed_buggy_data, file_name='processed_buggy_data.json')
    
#     return processed_buggy_data

def process_merge_data():
    processed_metrics_data = read_json_file('processed_metrics_data.json')
    labeled_buggy_data = read_json_file('labeled_buggy_data.json')
    
    merged_data = merge_data(processed_metrics_data, labeled_buggy_data, shuffle=False)
    
    return merged_data

def process_label_line_for_bug():
    processed_metrics_data = read_json_file('processed_metrics_data.json')
    
    line_processed_metrics_data = label_line_for_bug(data=processed_metrics_data)
    
    save_json_file(data=line_processed_metrics_data, file_name='line_processed_metrics_data.json')
    
    return line_processed_metrics_data

#########################################################################################################
def process_remove_fields(data, fields):
    return [
        {key: value for key, value in obj.items() if key not in fields}
        for obj in data
    ]
    
def process_metrics_data(file_name=None):
    if not file_name:
        file_name = 'metrics_data.json'
    
    metrics_data = read_json_file(file_name)
    
    return tokenize_and_encode_metrics_data(metrics_data)

def process_label_bug_positions():
    buggy_data = read_json_file('processed_buggy_data.json')
    metrics_data = read_json_file('processed_metrics_data.json')
    
    labeled_bug_data = label_bug_positions(buggy_data, metrics_data)
    
    save_json_file(data=labeled_bug_data, file_name='labeled_buggy_data.json')
    
    return labeled_bug_data
#########################################################################################################
def process_get_user_id_from_correct_src():
    data = read_json_file('train_data.json') + read_json_file('metrics_data.json')
    
    user_id_list = get_user_id(src_list=data)
    
    save_json_file(data=user_id_list, file_name='user_id_with_judge.json')
    
    return user_id_list

def process_group_judge_ids_by_user_id():
    data = read_json_file('user_id_with_judge.json')
    
    result = group_judge_ids_by_user_id(data)
    
    save_json_file(data=result, file_name='grouped_judge_ids.json')
    
    return result

def process_get_pairs():
    # Đọc dữ liệu từ file JSON
    data = read_json_file('grouped_judge_ids.json')
    
    # Số lượng thread (hoặc process) muốn sử dụng
    num_threads = 100  # Điều chỉnh số thread phù hợp với tài nguyên của bạn
    
    # Chia dữ liệu thành các phần nhỏ bên trong hàm
    chunk_size = ceil(len(data) / num_threads)
    data_chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    
    results = []
    
    # Sử dụng ThreadPoolExecutor để chạy song song các phần dữ liệu
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {executor.submit(get_pairs, chunk): chunk for chunk in data_chunks}
        for future in as_completed(futures):
            result = future.result()
            results.extend(result)  # Gộp kết quả từ từng thread
    
    # Lưu kết quả vào file JSON
    save_json_file(results, 'user_id_with_pairs.json')
    
    return results

def process_filter_pairs():
    data = read_json_file('user_id_with_pairs.json')
    
    result = filter_pairs_by_similarity(data)
    
    save_json_file(result, 'filtered_pairs.json')
    
    print(len(result))
    
    return result