class CTokenEncoder:

    def __init__(self):
        self.keyword_map = {
            'auto': 30, 'break': 31, 'case': 32, 'char': 33,
            'const': 34, 'continue': 35, 'default': 36, 'do': 37,
            'double': 38, 'else': 39, 'enum': 40, 'extern': 41,
            'float': 42, 'for': 43, 'goto': 44, 'if': 45,
            'int': 46, 'long': 47, 'register': 48, 'return': 49,
            'short': 50, 'signed': 51, 'sizeof': 52, 'static': 53,
            'struct': 54, 'switch': 55, 'typedef': 56, 'union': 57,
            'unsigned': 58, 'void': 59, 'volatile': 60, 'while': 61
        }
        self.punctuation_map = {
            '!': 63, '?': 64, '_': 65, '"': 66, '#': 67, '$': 68, '%': 69, '&': 70, 
            "'": 71, '(': 72, ')': 73, '*': 74, '+': 75, ',': 76, '-': 77, '.': 78,
            '/': 79, 
            ':': 90, ';': 91, '<': 92, '=': 93, '>': 94, '@': 95,
            '[': 122, '\\': 123, ']': 124, '^': 125, '`': 126,
            '{': 153, '|': 154, '}': 155, '~': 156
        }
        self.number_map = {
            '0': 80, '1': 81, '2': 82, '3': 83, '4': 84, '5': 85, '6': 86, '7': 87,
            '8': 88, '9': 89
        }
        self.alphabet_map = {
            'A': 96, 'B': 97, 'C': 98, 'D': 99, 'E': 100, 'F': 101, 'G': 102, 'H': 103, 
            'I': 104, 'J': 105, 'K': 106, 'L': 107, 'M': 108, 'N': 109, 'O': 110, 'P': 111, 
            'Q': 112, 'R': 113, 'S': 114, 'T': 115, 'U': 116, 'V': 117, 'W': 118, 'X': 119, 
            'Y': 120, 'Z': 121,
            'a': 127, 'b': 128, 'c': 129, 'd': 130, 'e': 131, 'f': 132, 'g': 133, 'h': 134, 
            'i': 135, 'j': 136, 'k': 137, 'l': 138, 'm': 139, 'n': 140, 'o': 141, 'p': 142, 
            'q': 143, 'r': 144, 's': 145, 't': 146, 'u': 147, 'v': 148, 'w': 149, 'x': 150, 
            'y': 151, 'z': 152
        }

        # Function: 0 - 9
        self.func_id = 0
        self.func_name_map = {}
        
        # Variable: 10 - 29
        self.var_id = 10
        self.var_name_map = {}
    
    def encode_tokens(self, token_list):
        encoded_tokens = []
        for token_type, token_value in token_list:
            # Keyword 
            if token_value in self.keyword_map:
                encoded_tokens.append(self.keyword_map[token_value])
            # Punctuation
            elif token_value in self.punctuation_map:
                encoded_tokens.append(self.punctuation_map[token_value])
            # Number
            elif token_value in self.number_map:
                encoded_tokens.append(self.number_map[token_value])
            # Alphabet
            elif token_value in self.alphabet_map:
                encoded_tokens.append(self.alphabet_map[token_value])
            # Function:
            elif token_type == 'FUNCTION':
                # Function name already exists
                if token_value in self.func_name_map:
                    encoded_tokens.append(self.func_name_map[token_value])
                # If not: 
                # 1. Map function name with current function id and save into func_name_map
                # 2. Increase func_id by 1
                else:
                    self.func_name_map[token_value] = self.func_id
                    encoded_tokens.append(self.func_id)
                    self.func_id += 1
                    # if self.func_id < 10:
                    #     self.func_id += 1
                    # else: # func_id >= 10
            # Variable:
            elif token_type == 'VARIABLE':
                # Variable name already exists
                if token_value in self.var_name_map:
                    encoded_tokens.append(self.var_name_map[token_value])
                # If not: 
                # 1. Map variable name with current variable id and save into var_name_map
                # 2. Increase var_id by 1
                else:
                    self.var_name_map[token_value] = self.var_id
                    encoded_tokens.append(self.var_id)
                    self.var_id += 1
            # Undefined case???
            else:
                encoded_tokens.append(-1)
                
        return encoded_tokens

    def reset_id(self):
        '''
        Reset current function and variable id to it initial value
        '''
        # Function: 0 - 9
        self.func_id = 0
        self.func_name_map = {}
        
        # Variable: 10 - 29
        self.var_id = 10
        self.var_name_map = {}

    def get_vocab_map(self):
        reversed_keyword_map = {v: k for k, v in self.keyword_map.items()}
        reversed_punctuation_and_symbol_map = {v: k for k, v in self.punctuation_and_symbol_map.items()}
        self.vocab_map = {**reversed_keyword_map, **reversed_punctuation_and_symbol_map, **self.literal_map}
        
        return self.vocab_map
