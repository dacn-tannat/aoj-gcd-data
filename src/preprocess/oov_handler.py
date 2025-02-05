# import numpy as np
# from scipy.spatial.distance import cosine
# from gensim.models import FastText
import json
from Levenshtein import distance as levenshtein_distance
from services.json_services import *

# def compute_character_similarity(token1, token2):
#     # Kiểm tra nếu cả hai token là số
#     try:
#         num1, num2 = float(token1), float(token2)
#         max_value = max(abs(num1), abs(num2), 1)  # Tránh chia cho 0
#         similarity = 1 - (abs(num1 - num2) / max_value)
#         return max(0.0, similarity)  # Đảm bảo similarity không âm
#     except ValueError:
#         pass  # Không phải số, tiếp tục xử lý như chuỗi

#     # Xử lý như string token
#     max_len = max(len(token1), len(token2))
#     if max_len == 0:
#         return 1.0  # Hai chuỗi rỗng coi như giống nhau hoàn toàn
#     levenshtein_dist = levenshtein_distance(token1, token2)
#     similarity = 1 - (levenshtein_dist / max_len)
#     return similarity

# def compute_semantic_similarity(token1, token2, model):
#     # Kiểm tra nếu token là số
#     try:
#         float(token1)
#         float(token2)
#         # Đối với số, sử dụng character similarity làm proxy cho semantic similarity
#         return compute_character_similarity(token1, token2)
#     except ValueError:
#         pass  # Không phải số, tiếp tục xử lý như string token

#     # Xử lý string token với Cosine Similarity
#     try:
#         vector1 = model.wv[token1]
#         vector2 = model.wv[token2]
#         similarity = 1 - cosine(vector1, vector2)  # Cosine similarity (-1, 1)
#         return (similarity + 1) / 2  # Chuẩn hóa về [0, 1]
#     except KeyError:
#         return 0  # Trường hợp token không có trong embedding

# def find_closest_token(oov_token, vocab_map, model, alpha=0.5):
#     max_total_similarity = -1  # Giá trị similarity tối đa tìm được
#     best_token = None  # Token có độ tương đồng cao nhất
#     best_encoding = None  # Mã hóa của token đó

#     for vocab_key, vocab_token in vocab_map.items():
#         # Tính Character Similarity
#         char_sim = compute_character_similarity(oov_token, vocab_token)

#         # Tính Semantic Similarity
#         try:
#             sem_sim = compute_semantic_similarity(oov_token, vocab_token, model)
#         except KeyError:
#             sem_sim = 0  # Nếu token không tồn tại trong embedding

#         # Tính tổng điểm similarity
#         total_similarity = alpha * char_sim + (1 - alpha) * sem_sim

#         if total_similarity > max_total_similarity:
#             max_total_similarity = total_similarity
#             best_token = vocab_token
#             best_encoding = vocab_key
            
#     return best_token, best_encoding

def find_closest_token(vocab, token):
    # vocab = read_json_file('vocab_map_data.json')
    # vocab_map = {int(k): v for k, v in vocab.items()}
    
    min_distance = float('inf')
    closest_token = None
    encoded_id = None

    for vocab_key, vocab_token in vocab.items():
        try:
            if isinstance(token, str) and isinstance(vocab_token, str):
                # Compare string values
                distance = levenshtein_distance(token, vocab_token)
            elif isinstance(token, (int, float)) and isinstance(vocab_token, (int, float)):
                # Compare numeric values
                distance = abs(float(token) - float(vocab_token))
            else:
                continue  # Skip mismatched types
        except ValueError:
            continue  # Skip invalid comparisons
        
        if distance < min_distance:
            min_distance = distance
            closest_token = vocab_token
            encoded_id = int(vocab_key)

    return closest_token, encoded_id

# def encode_metrics_source(raw_token_list):
#     vocab = read_json_file('vocab_map_data.json')
#     vocab_map = {int(k): v for k, v in vocab.items()}
    
#     encoded_tokens = []
    
#     for tok in raw_token_list:
#         found = False
#         encoded_id = None
#         for key, value in vocab_map.items():
#             if value == tok:
#                 encoded_id = int(key)
#                 found = True
#                 break
#         if found and encoded_id:
#             encoded_tokens.append(encoded_id)
            
#         if not found:
#             closest_token, encoded_id = find_closest_token(vocab_map, tok)
#             print(f'Meet OOV token at: {tok} -> ({closest_token}, {encoded_id})')
#             encoded_tokens.append(encoded_id)
    
#     return encoded_tokens

def test_handle_oov():
    oov_token_list = [128, "\"1 %d\"", "\"%%d%%d\"", "\"%f %f\"", "\"%%d\\n\"",
                      "\"%%d %%d\"", 500, "\": %s\\n\"", "\": %d\\n\"", 
                      "\"\u7bc4\u56f2\u5916\u3067\u3059\u3002\\n\"", "\"1\\n\"", 
                      100000, 13, "\"Error./n\"", 1000000001,
                      "\"Number should be less than 10^9! \\n\"",
                      "\"Number should be non-negative!\\n\"",
                      "\"Input data error!\\n\"", "\"data not enough! \\n\"",
                      "\"x,y\u306e\u5165\u529b\u304c\u7bc4\u56f2\u5916\u3067\u3059\\n\"",
                      22, "\"Please type 1 to 1000000000.\"",
                      "\"\u5165\u529b\u7bc4\u56f2\u5916\u3067\u3059\\n\"",
                      "\"%s\"", 15, "\"%\"", "\"%lu %lu\"", "\"%lld\"",
                      "\"\u6570\u5b57\u304c\u5927\u304d\u904e\u304e\u307e\u3059\u3002\\n\"",
                      32, 100005, "\"scanf: m, n\"", "\"\u5236\u7d04\u306e\u7bc4\u56f2\u5916\u3067\u3059\\n\"",
                      "\"stdio.h\"", "\"r\"", "\"input.txt\"", 404040,
                      "\"1<=x,y<=10^9\\n\"", "\"Error!!\\n\"",
                      "\"x = %i\\ny = %i\\n\"", "\"%lu\\n\"", 7,6,4
                      ]
    
    vocab = read_json_file('vocab_map_data.json')
    vocab_map = {int(k): v for k, v in vocab.items()}
   
    # # Tạo dữ liệu huấn luyện cho FastText
    # sentences = [list(token) for token in list(vocab_map.values()) + oov_token_list]  # Tách token thành danh sách ký tự

    # # Huấn luyện mô hình FastText
    # model = FastText(sentences, vector_size=50, min_count=1)
    
    for tok in oov_token_list:
        found = False
        encoded_id = None
        print("______________________________________________________________")
        for key, value in vocab_map.items():
            if value == tok:
                encoded_id = int(key)
                found = True
                break
        if found and encoded_id:
            print(f'{tok} is in vocabulary')
            print(f'Encoded ID for {tok} is {encoded_id}')
            
        if not found:
            print(f'{tok} is an OOV token!')
            # closest_token, encoded_id = find_closest_token(tok, vocab_map, model, alpha=0.5)
            closest_token, encoded_id = find_closest_token(vocab_map, tok)
            print(f'Closest token for {tok} is {closest_token} with {encoded_id = }')