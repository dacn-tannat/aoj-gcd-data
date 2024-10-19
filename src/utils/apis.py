import requests
from .constants import * 

def fetch_data_from_url(url):
    """
    Fetch JSON data from a given URL.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        dict: The JSON response from the URL.

    Raises:
        ValueError: If the request fails or returns a non-200 status code.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f'Failed to fetch from {url}\nStatus code: {response.status_code}')

def fetch_problem_submission_records(problem_id, problem_pagination = ''):
    """
    Fetch submission records for a specific problem.

    Args:
        problem_id (str): The ID of the problem to fetch submissions for.
        problem_pagination (str, optional): Pagination parameters for the request.

    Returns:
        dict: The JSON response containing submission records.

    Note:
        API endpoint: https://judgeapi.u-aizu.ac.jp/submission_records/problems/{problemID}?{page,size}
    """
    url = f'{BASE_URL}/{SUBMISSION_RECORDS}/{PROBLEMS}/{problem_id}'
    if problem_pagination: 
        url += f'?{problem_pagination}'
        
    return fetch_data_from_url(url)

def fetch_review_by_judge_id(judge_id):
    """
    Fetch a review for a specific judge ID.

    Args:
        judge_id (str): The ID of the judge to fetch the review for.

    Returns:
        dict: The JSON response containing the review.

    Note:
        API endpoint: https://judgeapi.u-aizu.ac.jp/reviews/{judgeID}
    """
    url = f'{BASE_URL}/{REVIEWS}/{judge_id}'
    return fetch_data_from_url(url)
