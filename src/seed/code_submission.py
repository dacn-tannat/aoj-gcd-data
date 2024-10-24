import requests
import time
from utils.apis import *
from services.json_services import *

MAX_RETRIES = 100

def submit_code_and_validate(session, source_code):

    # Submit code
    payload = {
        "problemId": GCD_PROBLEM_ID,
        "language": C_LANGUAGE,
        "sourceCode": source_code
    }    

    # print(f'Sleep for {SLEEP_TIME} to avoid rate limit')
    # time.sleep(10)
    # submission_token = submit_code(session, payload)
    # if (submission_token):
    #     print('Submit code successfully\nsubmission_token: ', submission_token)
    
    retries = 0
    while retries < MAX_RETRIES:
        print('\nAttempting to submit code...')
        submission_token = submit_code(session, payload)
        if (submission_token):
            print('Submit code successfully')
            break
        else:
            print('An error occurred! Retry in 5s...')
            time.sleep(5)
            retries += 1
            print(f'Number of retries: {retries}')
        

    if (not submission_token):
        raise ConnectionError('Rate limit reached!')

    # Sleep 5s
    print('Wait for 5s before fetching data...')
    time.sleep(5)
    
    # Get last 100 submissions
    print('Attempting to fetch last 100 submissions...')
    last_100_submissions = get_last_100_submissions()
    if (last_100_submissions):
        print('Fetching last 100 submissions successfully')
    else:
        raise ValueError(f'An error occurred while fetching last 100 submissions')
    
    # Find submission
    if (submission_token and last_100_submissions):
        for submission in last_100_submissions:
            if submission.get('token') == submission_token.get('token'):
                submitted_code = submission
                break
    else:
        raise ValueError('Something went wrong: Cannot find submission_token or last_100_submissions')
        
    # Get status and accuracy of submitted code
    if submitted_code:
        status = submitted_code.get('status')
    
    # Conditions check:
        is_wrong_answer = status == 1
        # does_not_pass_all_test_cases = accuracy.split('/')[0] < accuracy.split('/')[1]
        
        if (is_wrong_answer):
            print('-----VALID------')
            return True
        else:
            print('-----INVALID------')
            return False
            
            
    else:
        raise ValueError('Something went wrong, cannot find submitted_code')

def filter_valid_codes_from_erroneous_data():
    session = requests.Session()
    user_info = login_to_aoj(session)
    
    if (user_info):
        erroneous_data = read_json_file('erroneous_raw_data_c.json')
        processed_erroneous_data = []
        for data in erroneous_data:
            # Create a new list to store the source codes that return 1
            new_source_codes = []
            if data and data.get('source_codes'):
                for obj in data.get('source_codes'):
                    if (type(obj) == str):
                        source_code = obj
                    elif (type(obj) == dict):
                        if (obj.get('source_code')): source_code = obj.get('source_code')
                        elif (obj.get('code')): source_code = obj.get('source_code')
                        else:
                            raise ValueError('Unable to find source code!')
                    else: ValueError('Invalid object')
                    
                    result = submit_code_and_validate(session, source_code)
                    if result:
                        new_source_codes.append(source_code)
                if new_source_codes:
                    processed_erroneous_data.append({
                        'judge_id': data.get('judge_id'),
                        'source_codes': new_source_codes
                    })
                print('Sleep for 5s before moving to the next object')
                time.sleep(10)
        save_json_file(processed_erroneous_data, 'erroneous_processed_data_c.json')
    
    else:
        print('Unable to log in')