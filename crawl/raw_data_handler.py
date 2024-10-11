from .constants import *
from .fetch import fetch_problem_submission_records
from .review_handler import handle_review_data_with_threads
from services.json_services import save_json_file

def get_raw_data():
    submission_records = fetch_problem_submission_records(GCD_PROBLEM_ID, GCD_PAGINATION)
    judge_ids = [
        { 
            'judgeId': submission.get('judgeId'), 
            'status': submission.get('status')
        }
        for submission in submission_records 
        if submission.get('language') == C_LANGUAGE
    ]
    raw_data = handle_review_data_with_threads(judge_ids)
    
    save_json_file(data=raw_data, file_path='raw_data_c2.json')
    
    return raw_data