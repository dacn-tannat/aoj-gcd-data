import re
from .lexer.CLexer import CLexer
from .encoder.CTokenEncoder import CTokenEncoder

def filter(src_list):
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

def tokenize_and_encode(src_list):
    """
    Tokenize and encode the source code in the given list.

    Args:
        src_list (list): A list of dictionaries containing source code information.

    Returns:
        list: A filtered list of dictionaries with added 'raw_tokens' and 'encoded_tokens' fields.

    This function performs the following steps for each source code entry:
    1. Tokenizes the source code using CLexer.
    2. Extracts the token values and adds them to the entry as 'raw_tokens'.
    3. Encodes the raw tokens into a numerical format using CTokenEncoder.
    4. Adds the encoded tokens to the entry as 'encoded_tokens'.
    5. Filters the processed list to remove invalid entries.

    Note:
        This function modifies the input list in-place before filtering.
    """
    lexer = CLexer()
    encoder = CTokenEncoder()
    for src in src_list:
        source_code = src['source_code']
        
        encoder.reset_id()
        
        # Tokenize source code into raw tokens
        raw_tokens = lexer.tokenize(source_code)
        raw_tokens_value = [token[1] for token in raw_tokens]
        src['raw_tokens'] = raw_tokens_value
        
        # Encode raw tokens into numerical format
        encoded_tokens = encoder.encode_tokens(raw_tokens)
        src['encoded_tokens'] = encoded_tokens
    
    literal_map = encoder.get_literal_map()
    filter_src_list = filter(src_list)
    
    return literal_map, filter_src_list
