import re
from .lexer.CLexer import CLexer
from .encoder.CTokenEncoder import CTokenEncoder

def clean_and_format(source_code):
    source_code = re.sub(r'\n|\t|\r', ' ', source_code)
    source_code = re.sub(r'\s+', ' ', source_code)
    source_code = source_code.strip()
    return source_code

def filter(src_list):
    filtered_data = [
        src for src in src_list if (
            src.get('raw_tokens') 
            and 
            not re.search(r'[^\x00-\x7F]', src['sourceCode']) 
            and
            not "Last login" in src['sourceCode']
        )
    ]
    return filtered_data

def tokenize_and_encode(src_list):
    lexer = CLexer()
    encoder = CTokenEncoder()
    for src in src_list:
        source_code = src['sourceCode']
        # formatted_code = clean_and_format(source_code)
        
        # Tokenize source code into raw tokens
        raw_tokens = lexer.tokenize(source_code)
        raw_tokens_value = [token[1] for token in raw_tokens]
        src['raw_tokens'] = raw_tokens_value
        
        # Encode raw tokens into numerical format
        encoded_tokens = encoder.encode_tokens(raw_tokens)
        src['encoded_tokens'] = encoded_tokens
    
    print('Error characters: ', lexer.get_error_characters())
    return filter(src_list)