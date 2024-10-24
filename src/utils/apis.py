import requests
from .constants import * 

def get_data_from_url(url):
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
        print(f'Failed to fetch from {url}\nResponse: {response.json()}')
        return None

def post_data_to_url(session, url, payload, headers=None):
    """
    Send a POST request to a specified URL using a session with given payload and headers.

    Args:
        session (requests.Session): The session object to manage cookies and persistent state.
        url (str): The URL to send the POST request to.
        payload (dict): The data to send in the POST request body.
        headers (dict, optional): The request headers to include.

    Returns:
        dict: The JSON response from the URL.

    Raises:
        ValueError: If the request fails or returns a non-200 status code.
    """
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
        
    return get_data_from_url(url)

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
    return get_data_from_url(url)

def get_self(session):
    """
    Make a GET request to retrieve the self user information.

    Args:
        session (requests.Session): The session object containing the logged-in user's cookies.

    Returns:
        dict: The JSON response containing self user details.
    """
    url = f'{BASE_URL}/{SELF}'
    response = session.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f'Failed to get self info.\nStatus code: {response.status_code}')

def login_to_aoj(session):
    """
    Log in to the Aizu Online Judge using user credentials and store the session.

    Args:
        session (requests.Session): The session object to manage cookies and persistent state.

    Returns:
        dict: The JSON response containing session details.

    Raises:
        ValueError: If login fails or returns a non-200 status code.
    """
    import os
    from dotenv import load_dotenv
    
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

def submit_code(session, payload):
    """
    Submit source code to Aizu Online Judge.

    Args:
        session (requests.Session): The session object containing the logged-in user's cookies.
        problem_id (str): The ID of the problem to submit the solution for.
        language (str): The programming language of the source code (e.g., "C++").
        source_code (str): The source code to be submitted.

    Returns:
        dict: The JSON response containing the submission token.

    Raises:
        ValueError: If the submission fails or returns a non-200 status code.
    """
    url = f'{BASE_URL}/{SUBMISSIONS}'

    return post_data_to_url(session, url, payload)
    
def get_last_100_submissions():
    url = f'{BASE_URL}/{SUBMISSION_RECORDS}/{RECENT}'
    
    return get_data_from_url(url)
    