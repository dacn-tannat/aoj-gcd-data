import time
from utils.apis import *
from services.json_services import *

MAX_RETRIES = 10

def submit(session, source_code):
    # Submit code
    payload = {
        "problemId": GCD_PROBLEM_ID,
        "language": C_LANGUAGE,
        "sourceCode": source_code
    }
    
    retries = 1
    while retries < MAX_RETRIES:
        print('\nAttempting to submit code...')
        submission_token = submit_source_code(session, payload)
        if (submission_token):
            print('Submit code successfully')
            break
        else:
            print(f'An error occurred! Retry in 5s...\nNumber of retries: {retries}/{MAX_RETRIES}')
            retries += 1
            time.sleep(5)
        
    if (not submission_token):
        print('An error occurred while submitting code: Cannot find submission_token')
        return None

    # Sleep 5s
    print('Wait for 5s before fetching data again...')
    time.sleep(5)
    
    # Get last 100 submissions
    print('Attempting to fetch last 100 submissions...')
    last_100_submissions = get_last_100_submissions()
    if (last_100_submissions):
        print('Fetching last 100 submissions successfully')
    else:
        print('An error occurred while fetching the last 100 submissions')
        return None
    
    return (submission_token.get('token'), last_100_submissions)

def get_submission(session, source_code):
    result = submit(session, source_code)
    
    if result: 
        submission_token, last_100_submissions = result
        for submission in last_100_submissions:
            if (submission_token == submission.get('token')):
                return submission
    else:
        print(f'Cannot find submission by submission_token {submission_token}')
        return None
    
def is_valid_submission(submission):
    if submission:
        status = submission.get('status')
        
        if status == 1: 
            print('\tValid!')
            return True
        else: 
            print('\tInvalid')
            return False
    
    else:
        return False
    
def validate_and_filter_valid_buggy_data(buggy_data, allow_duplicate=False):
    session = requests.Session()
    
    # Login to AOJ
    user_info = login_to_aoj(session)
    
    if (user_info):
        processed_buggy_data = []
        for buggy_obj in buggy_data:
            if buggy_obj.get('source_codes'):
                buggy_src_list = buggy_obj.get('source_codes')
                for src in buggy_src_list:
                    submission_info = get_submission(session, src)
                    if is_valid_submission(submission_info):
                        processed_buggy_data.append({
                            'judge_id': buggy_obj.get('judge_id'),
                            'source_code': src
                        })
                        if not allow_duplicate:
                            break
            print('Sleep for 10s before moving to the next object')
            time.sleep(10)

        if (len(processed_buggy_data)):            
            return processed_buggy_data
        
    else:
        print('Login unsuccessful')
        return []
                    
                        
                