import re
from .lexer.CLexer import CLexer
from .encoder.CTokenEncoder import CTokenEncoder
from services.json_services import *
from .oov_handler import *

def filter_invalid_source_codes(src_list):
    """
    Filter the source code list to remove entries with invalid or unwanted content.

    Args:
        src_list (list): A list of dictionaries containing source code information.

    Returns:
        list: A filtered list of dictionaries, excluding entries that:
            - Don't have raw tokens
            - Contain non-ASCII characters
            - Contain the phrase "Last login"

    Note:
        This function is used to clean the dataset by removing potentially problematic entries.
    """
    filtered_data = [
        src for src in src_list if (
            src.get('raw_tokens') 
            and 
            not re.search(r'[^\x00-\x7F]', src['source_code']) 
            and
            not "Last login" in src['source_code']
        )
    ]
    return filtered_data

def tokenize_and_encode_train_data(src_list):
    lexer = CLexer()
    encoder = CTokenEncoder()
    for src in src_list:
        source_code = src['source_code']
        
        encoder.reset_id()
        
        # Tokenize source code into raw tokens
        raw_tokens = lexer.tokenize(source_code) # list of (token_type, token_value)
        raw_tokens_value = [token[1] for token in raw_tokens] 
        src['raw_tokens'] = raw_tokens_value
        
        # Encode raw tokens into numerical format
        encoded_tokens = encoder.encode_tokens(raw_tokens)
        src['encoded_tokens'] = encoded_tokens
    
    vocab_map = encoder.get_vocab_map()
    literal_map = encoder.get_literal_map()
    filter_src_list = filter_invalid_source_codes(src_list)
    
    return filter_src_list, vocab_map, literal_map

def tokenize_and_encode_metrics_data(src_list):
    lexer = CLexer()
    literal_map = read_json_file(file_name='literal_map_data.json')
    encoder = CTokenEncoder(literal_map=literal_map)
    
    for src in src_list: 
        source_code = src['source_code']
        
        encoder.reset_id()
        
        # Tokenize source code into raw tokens
        raw_tokens = lexer.tokenize(source_code) # list of (token_type, token_value)
        raw_tokens_value = [token[1] for token in raw_tokens] # list of token_value
        src['raw_tokens'] = raw_tokens_value
        
        # Encode raw token into numerical token, by using vocab
        encoded_tokens = encoder.encode_tokens(raw_tokens, is_train_data=False)
        src['encoded_tokens'] = encoded_tokens
        
        # Get oov_tokens
        oov_tokens = encoder.get_oov_tokens()
        
    return src_list, oov_tokens

        
        
    