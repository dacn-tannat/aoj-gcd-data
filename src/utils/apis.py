import requests
from .constants import * 

import os
from dotenv import load_dotenv

import aiohttp

async def get_data_from_url_async(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, ssl=False) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f'Failed to fetch from {url}\nResponse: {await response.text()}')
                    return None
        except aiohttp.ClientError as e:
            print(f'Client error occurred: {e}')
            return None

def get_data_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to fetch from {url}\nResponse: {response.json()}')
        return None

def post_data_to_url(session, url, payload, headers=None):
    if session is None:
        session = requests.Session()
    
    if headers is None: 
        headers = {
            "Content-Type": "application/json"
        }

    response = session.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to post to {url}\nResponse: {response.json()}')
        return None

def fetch_problem_submission_records(problem_id, problem_pagination = ''):
    url = f'{BASE_URL}/{SUBMISSION_RECORDS}/{PROBLEMS}/{problem_id}'
    if problem_pagination: 
        url += f'?{problem_pagination}'
        
    return get_data_from_url(url)

def fetch_review_by_judge_id(judge_id):
    url = f'{BASE_URL}/{REVIEWS}/{judge_id}'
    
    return get_data_from_url(url)

def get_self(session):
    url = f'{BASE_URL}/{SELF}'
    response = session.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f'Failed to get self info.\nStatus code: {response.status_code}')

def login_to_aoj(session):
    load_dotenv()
    
    url = f'{BASE_URL}/{SESSION}'
    payload = {
        "id": os.getenv('AOJ_ID'),
        "password": os.getenv('AOJ_PASSWORD')
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    return post_data_to_url(session, url, payload, headers)

def submit_source_code(session, payload):
    url = f'{BASE_URL}/{SUBMISSIONS}'

    return post_data_to_url(session, url, payload)
    
def get_last_100_submissions():
    url = f'{BASE_URL}/{SUBMISSION_RECORDS}/{RECENT}'
    
    return get_data_from_url(url)

async def get_verdict_by_judge_id(judge_id):
    url = f'{BASE_URL}/{VERDICTS}/{judge_id}'
    
    return await get_data_from_url_async(url)

def get_submission_record(user_id, problem_id='ALDS1_1_B'):
    default_pagination = 'page=0&size=10000000'
    url = f'{BASE_URL}/{SUBMISSION_RECORDS}/{USERS}/{user_id}/{PROBLEMS}/{problem_id}?{default_pagination}'
    
    return get_data_from_url(url)