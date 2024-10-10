import requests
from constants import * 

def fetch_data_from_url(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f'Failed to fetch from {url}\nStatus code: {response.status_code}')

def fetch_problem_submission_records(problem_id: str, problem_pagination: str = ''):
    '''
    https://judgeapi.u-aizu.ac.jp/submission_records/problems/{problemID}?{page,size}
    '''
    url = f'{BASE_URL}/{SUBMISSION_RECORDS}/{PROBLEMS}/{problem_id}'
    if problem_pagination: 
        url += f'?{problem_pagination}'
        
    return fetch_data_from_url(url)

def fetch_review_by_judge_id(judge_id: str):
    '''
    https://judgeapi.u-aizu.ac.jp/reviews/{judgeID}
    '''
    url = f'{BASE_URL}/{REVIEWS}/{judge_id}'
    return fetch_data_from_url(url)
