from .constants import *
from .fetch import fetch_problem_submission_records
from .review_handler import handle_review_data_with_threads
from services.json_services import save_json_file

def get_raw_data():
    """
    Fetch and process raw data for the GCD problem submissions.

    This function performs the following steps:
    1. Fetches submission records for the GCD problem.
    2. Filters submissions to include only those in C language.
    3. Extracts judge IDs and statuses from the filtered submissions.
    4. Handles review data for the extracted judge IDs using multithreading.
    5. Saves the processed raw data to a JSON file.

    Returns:
        list: A list of processed review data for C language submissions.

    Note:
        The raw data is saved to 'raw_data_c2.json' in the data directory.
    """
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
    
    save_json_file(data=raw_data, file_name='raw_data_c2.json')
    
    return raw_data
