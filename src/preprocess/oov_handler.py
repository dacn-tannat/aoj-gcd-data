import Levenshtein
from services.json_services import *


def find_closest_token(vocab, token):
    min_distance = float('inf')
    closest_token = None

    for vocab_key, vocab_token in vocab.items():
        # Chỉ so sánh với literals (chuỗi hoặc số)
        if isinstance(vocab_token, str):
            distance = Levenshtein.distance(token, vocab_token)
        elif isinstance(vocab_token, int):
            distance = abs(float(token) - float(vocab_token))
        else: 
            raise TypeError(f'Cannot resolve for OOV token: {token}')
        
        if distance < min_distance:
            min_distance = distance
            closest_token = vocab_token

    return closest_token, min_distance

def handle_oov(token):
    vocab = read_json_file('vocab_map_data.json')
    vocab_map = {int(k): v for k, v in vocab.items()}
    return find_closest_token(vocab_map, token)
