import requests
from utils.apis import *

def submit_code_and_validate(source_code=None):

    session = requests.Session()
            
    # Login
    try: 
        print('Attempting to log in...')
        user_info = login_to_aoj(session)
        print('Login successful\nuser_info: ', user_info)
    except ValueError as e:
        raise ValueError(f'An error occurred while logging in: {e}')

    # Submit code
    submission_token = {}
    try:
        print('\nAttempting to submit code...')
        payload = {
            "problemId": GCD_PROBLEM_ID,
            "language": C_LANGUAGE,
            "sourceCode": source_code if source_code is not None else GCD_SOURCE_ACCEPTED_CODE
        }
        submission_token = submit_code(session, payload)
        print('Submit code successfully\nsubmission_token: ', submission_token)
        
    except ValueError as e:
        raise ValueError(f'An error occurred while submitting code: {e}')
        
    # Get last 100 submissions
    last_100_submissions = []
    try:
        print('\nAttempting to fetch last 100 submissions...')
        last_100_submissions = get_last_100_submissions()
        print('Fetching last 100 submissions successfully')
    except ValueError as e:
        print(f'An error occurred while fetching last 100 submissions: {e}')
    
    # Find submission
    if (submission_token and last_100_submissions):
        for submission in last_100_submissions:
            if submission.get('token') == submission_token.get('token'):
                submitted_code = submission
                break
    else:
        print('Something went wrong, cannot find submission_token or last_100_submissions')
        
    # Get status and accuracy of submitted code
    status, accuracy = submitted_code.get('status'), submitted_code.get('accuracy')
    
    # Conditions check:
    is_not_compile_error = status not in [0,4]
    does_not_pass_all_test_cases = accuracy.split('/')[0] < accuracy.split('/')[1]
    
    if (is_not_compile_error and does_not_pass_all_test_cases):
        print('Valid source code')
        # Handle this case later, maybe write into a json file
    else: 
        print('Invalid source code')
    