import re
from preprocess import *
from utils.json_handler import *

def process_data():
    src_list = read_json_file('raw_data_c.json')
    print('Preprocessing raw_data.json...')
    preprocessed_data = tokenize_and_encode(src_list)
    save_json_file(preprocessed_data, 'preprocessed_data_c.json')
    
    avg_token = calculate_average_tokens(preprocessed_data, 'preprocessed_data_c.json')
    print('Average tokens (all): ', avg_token)
    avg_token_4 = calculate_average_tokens(preprocessed_data, 'preprocessed_data_c.json', 4)
    print('Average tokens (status=4): ', avg_token_4)
    

    print('Data saved to preprocessed_data.json successfully.')

def gen_tokens():
    src = '''
    #include <stdio.h>

    int gcd(int, int);

    int main() {
        int a, b;
        scanf("%d %d", &a, &b);
        printf("%d\n", gcd(a, b));
        return 0;
    }

    int gcd(int x, int y) {
        return y ? gcd(y, x % y) : x;
    }
    '''

    lexer = CLexer()
    encoder = CTokenEncoder()
    format_src = clean_and_format(src)

    raw_tokens = lexer.tokenize(format_src)
    numerical_tokens = encoder.encode_tokens(raw_tokens)

    for i in range(len(numerical_tokens)):
        print(f'{i}\t{raw_tokens[i][1]}\t{numerical_tokens[i]}')
        
    raw_tokens_value = [token[1] for token in raw_tokens]
    print(len(raw_tokens_value) == len(numerical_tokens))
    print('Raw tokens: ', raw_tokens_value)
    print('Encoded tokens:', numerical_tokens)

if __name__ == '__main__':
    # process_data()
    gen_tokens()
    # check_non_alphabetic_source_code('raw_data_c.json')
    
# Analyze:
# {
#     4: 4316, 
#     8: 1261, 
#     2: 1115, 
#     1: 2703, 
#     0: 1482, 
#     7: 734, 
#     -1: 3, ???????????
#     6: 2
# }