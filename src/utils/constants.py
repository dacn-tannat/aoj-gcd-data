"""
Constants used throughout the crawling process.

This module defines various constants used for API endpoints, problem identifiers,
pagination parameters, and programming language specifications.
"""

BASE_URL = 'https://judgeapi.u-aizu.ac.jp'
SUBMISSION_RECORDS = 'submission_records'
PROBLEMS = 'problems'
REVIEWS = 'reviews'
VERDICTS = 'verdicts'
USERS = 'users'

# Submit code
SELF = 'self'
SESSION = 'session'
SUBMISSIONS = 'submissions'
RECENT = 'recent'

# Programming language
C_LANGUAGE = 'C'

# Problem ID
GCD_PROBLEM_ID = 'ALDS1_1_B' 
GCD_PAGINATION = 'page=0&size=41685'

# Default GCD sources code
GCD_SOURCE_ACCEPTED_CODE = "int main()\n{\n    int x, y;\n    scanf(\"%d %d\", &x, &y);\n\n    int gcd;\n    while (x != 0)\n    {\n        gcd = x / y;\n        x = gcd;\n        y = x;\n        //printf(\"x:%d,y:%d\", x, y);\n    }\n    printf(\"%d\n\", y);\n}"
