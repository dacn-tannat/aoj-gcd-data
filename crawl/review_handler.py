from concurrent.futures import ThreadPoolExecutor, as_completed
from fetch import *

def get_review_data(judge_id: str):
    review = fetch_review_by_judge_id(judge_id)
    
    if review and review.get('policy') != 'private' and review.get('sourceCode'):
        return {
            'judge_id': judge_id,
            'source_code': review.get('sourceCode'),
            'status': review.get('status')
        }
    else: 
        return None
    
def handle_review_data_with_threads(judge_ids: list, num_threads=100):
    print(f'In progress of handling review data with {num_threads} threads')
    
    src_list = []
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_review = {executor.submit(get_review_data, judge['judgeId'], judge['status']): judge for judge in judge_ids}
        for future in as_completed(future_to_review):
            review = future_to_review[future]
            try:
                data = future.result()
                if data:
                    src_list.append(data)
            except Exception as exc:
                print(f'Judge ID {review["judgeId"]} generated an exception: {exc}')
    print(f'Handling review data: Done!')
    
    return src_list