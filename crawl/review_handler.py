from concurrent.futures import ThreadPoolExecutor, as_completed
from .fetch import *

def get_review_data(judge_id, status):
    """
    Fetch and process review data for a given judge ID.

    Args:
        judge_id (str): The ID of the judge to fetch the review for.
        status (str): The status of the submission.

    Returns:
        dict: A dictionary containing the judge_id, source_code, and status if the review is valid and public.
        None: If the review is private or doesn't contain source code.
    """
    review = fetch_review_by_judge_id(judge_id)
    
    if review and review.get('policy') != 'private' and review.get('sourceCode'):
        return {
            'judge_id': judge_id,
            'source_code': review.get('sourceCode'),
            'status': status
        }
    else: 
        return None
    
def handle_review_data_with_threads(judge_ids: list, num_threads=100):
    """
    Handle review data fetching and processing using multi-threading.

    Args:
        judge_ids (list): A list of dictionaries containing judge IDs and their statuses.
        num_threads (int, optional): The number of threads to use for parallel processing. Defaults to 100.

    Returns:
        list: A list of processed review data dictionaries.

    Note:
        This function uses ThreadPoolExecutor to fetch and process review data in parallel,
        which can significantly speed up the data collection process for large numbers of reviews.
    """
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
