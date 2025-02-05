from utils.apis import *
from services.json_services import *
from preprocess import CustomCLexer, CTokenEncoder

def get_user_id(src_list):
    user_id_list = []
    for src in src_list:
        judge_id = src.get('judge_id')
        response = fetch_review_by_judge_id(judge_id)
        if response.get('userId'):
            user_id_list.append({
                'user_id': response.get('userId'),
                'judge_id': judge_id
            })
    
    return user_id_list

def group_judge_ids_by_user_id(data): # [ { user_id: , judge_id: }, ... ]
    grouped = {}
    for item in data:
        user_id = item["user_id"]
        judge_id = item["judge_id"]

        if user_id not in grouped:
            grouped[user_id] = []
        grouped[user_id].append(judge_id)

    # Chuyển dictionary thành danh sách đối tượng như mong muốn
    result = [{"user_id": user_id, "judge_id": jids} for user_id, jids in grouped.items()]
    return result

def get_pairs(data_chunk):
    """
    Xử lý một phần nhỏ của dữ liệu (chunk) để tạo các cặp (pairs).
    """
    result = []
    num_pairs = 0

    for item in data_chunk:  # Mỗi item là { user_id: ..., judge_id: [...] }
        user_id = item.get('user_id')
        print('Processing user_id: ', user_id)

        submission_records = get_submission_record(user_id)
        if submission_records:
            correct_answers = [
                sub for sub in submission_records if sub["status"] == 4 and sub["language"] == 'C'
            ]
            wrong_answers = [
                sub for sub in submission_records if sub["status"] == 1 and sub["language"] == 'C'
            ]

            pairs = []
            for wrong_answer in wrong_answers:
                wrong_answer_judge_id = wrong_answer.get('judgeId')
                wrong_answer_source = fetch_review_by_judge_id(wrong_answer_judge_id).get('sourceCode')
                wrong_answer_encoded_token = get_encoded_tokens(wrong_answer_source)

                for correct_answer in correct_answers:
                    correct_answer_judge_id = correct_answer.get('judgeId')
                    correct_answer_source = fetch_review_by_judge_id(correct_answer_judge_id).get('sourceCode')
                    correct_answer_encoded_token = get_encoded_tokens(correct_answer_source)

                    pairs.append({
                        'correct_answer': {
                            'judge_id': correct_answer_judge_id,
                            'source_code': correct_answer_source,
                            'timestamp': correct_answer.get('judgeDate'),
                            'accuracy': correct_answer.get('accuracy')
                        },
                        'wrong_answer': {
                            'judge_id': wrong_answer_judge_id,
                            'source_code': wrong_answer_source,
                            'timestamp': wrong_answer.get('judgeDate'),
                            'accuracy': wrong_answer.get('accuracy')
                        },
                        'similarity': calc_lcs_similarity(correct_answer_encoded_token,
                                                          wrong_answer_encoded_token)
                    })

            if pairs:
                num_pairs += len(pairs)
                result.append({
                    'user_id': user_id,
                    'pairs': pairs
                })

    print('Number of pairs processed in chunk: ', num_pairs)
    return result

# phan tich ra token: CustomCLexer -> CEncoder
def get_encoded_tokens(src):
    lexer = CustomCLexer()
    encoder = CTokenEncoder()
    
    raw_tokens = lexer.tokenize(src)
    encoded_tokens = encoder.encode_tokens(raw_tokens)
    
    return encoded_tokens

# do do tuong dong 2 chuoi
def calc_lcs_similarity(list1, list2):
    m, n = len(list1), len(list2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if list1[i-1] == list2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    lcs_length = dp[m][n]
    similarity = 2 * lcs_length / (m + n)
    return similarity

def filter_pairs_by_similarity(data, similarity_threshold=0.85):
    result = []
    for item in data:
        pairs = item.get('pairs')
        filtered_pairs = [pair for pair in pairs if pair.get('similarity') > similarity_threshold]
        if len(filtered_pairs) > 0:
            result.append({
                'user_id': item.get('user_id'),
                'pairs': filtered_pairs
            })
    return result
    




def mini_test():
    data = {
    "user_id": "chyj256785115",
    "pairs": [
      {
        "correct_answer_judge_id": 9586212,
        "wrong_answer_ans_judge_id": 9586210
      }
    ]
  }
    lexer = CustomCLexer()
    encoder = CTokenEncoder()
    
    user_id = data.get('user_id')
    pairs = data.get('pairs')
    for pair in pairs:
        correct_judge_id = pair.get('correct_answer_judge_id')
        wrong_judge_id = pair.get('wrong_answer_ans_judge_id')
        
        correct_src_code = fetch_review_by_judge_id(correct_judge_id).get('sourceCode')
        wrong_src_code = fetch_review_by_judge_id(wrong_judge_id).get('sourceCode')
        
        correct_encoded_tokens = encoder.encode_tokens(lexer.tokenize(correct_src_code))
        wrong_encoded_tokens = encoder.encode_tokens(lexer.tokenize(wrong_src_code))
        
        print('similarity: ', calc_lcs_similarity(list1=correct_encoded_tokens, list2=wrong_encoded_tokens))