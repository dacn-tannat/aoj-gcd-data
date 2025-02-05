# from ..oov_handler import *

# class CTokenEncoder:
#     """
#     A class for encoding C language tokens into numerical representations.

#     This encoder maintains mappings for keywords, special characters, identifiers, and literals.
#     It assigns unique numerical codes to each token type for efficient processing and analysis.
#     """

#     def __init__(self, literal_map=None):
#         """
#         Initialize the CTokenEncoder with predefined mappings for keywords and special characters.

#         The encoder also initializes empty mappings for identifiers and literals,
#         which will be populated as new tokens are encountered during encoding.
#         """
#         self.keyword_map = {
#             'auto': 10, 'break': 11, 'case': 12, 'char': 13,
#             'const': 14, 'continue': 15, 'default': 16, 'do': 17,
#             'double': 18, 'else': 19, 'enum': 20, 'extern': 21,
#             'float': 22, 'for': 23, 'goto': 24, 'if': 25,
#             'int': 26, 'long': 27, 'register': 28, 'return': 29,
#             'short': 30, 'signed': 31, 'sizeof': 32, 'static': 33,
#             'struct': 34, 'switch': 35, 'typedef': 36, 'union': 37,
#             'unsigned': 38, 'void': 39, 'volatile': 40, 'while': 41
#         }
#         self.special_character_map = {
#             # Condition
#             'QMARK': 45, 'COLON': 46, 
#             # Member access
#             'ARROW': 48, 'PERIOD': 49,
#             # Miscellaneous
#             'ESCAPE': 51, 'HASH': 52, 
#             # EQUAL
#             'EQUALS': 54, 
#             # Arithmetic
#             'PLUS': 55, 'MINUS': 56, 'TIMES': 57, 'DIVIDE': 58, 'MODULO': 59,
#             # Arithmetic assignment
#             'PLUSEQUAL': 60, 'MINUSEQUAL': 61, 'TIMESEQUAL': 62, 'DIVIDEEQUAL': 63, 'MODEQUAL': 64,
#             # Relational 
#             'EQ': 65, 'NE': 66, 'LT': 67, 'GT': 68,  'LE': 69, 'GE': 70, 
#             # Increment & Decrement
#             'PLUSPLUS': 71, 'MINUSMINUS': 72, 
#             # Logical
#             'NOT': 75, 'AND': 76, 'OR': 77, 
#             # Bitwise
#             'BITWISE_NOT': 80, 'BITWISE_AND': 81, 'BITWISE_OR': 82, 'BITWISE_XOR': 83, 'LSHIFT': 84, 'RSHIFT': 85, 
#             # Bitwise assignment
#             'ANDEQUAL': 86, 'OREQUAL': 87, 'XOREQUAL': 88, 'LSHIFTEQUAL': 89, 'RSHIFTEQUAL': 90, 
#             # Separator
#             'SEMICOLON': 91, 'COMMA': 92, 'LBRACKET': 93, 'RBRACKET': 94,
#             'LPAREN': 96, 'RPAREN': 97, 'LBRACE': 98, 'RBRACE': 99
#         }
        
#         self.punctuation_and_symbol_map = {
#             '?': 45, ':': 46, # Condition
#             '->': 48, '.': 49, # Member access
#             '\\': 51, '#': 52, # Miscellaneous
#             '=': 54, # EQUAL
#             '+': 55, '-': 56, '*': 57, '/': 58, '%': 59, # Arithmetic
#             '+=': 60, '-=': 61, '*=': 62, '/=': 63, '%=': 64, # Arithmetic assignment
#             '==': 65, '!=': 66, '<': 67, '>': 68, '<=': 69, '>=': 70, # Relational
#             '++': 71, '--': 72, # Increment & Decrement
#             '!': 75, '&&': 76, '||': 77, # Logical
#             '~': 80, '&': 81, '|': 82, '^': 83, '<<': 84, '>>': 85, # Bitwise
#             '&=': 86, '|=': 87, '^=': 88, '<<=': 89, '>>=': 90, # Bitwise assignment
#             ';': 91, ',': 92, '[': 93, ']': 94, # Separator
#             '(': 96, ')': 97, '{': 98, '}': 99 # Parentheses and braces
#         }
        
#         self.id_map = {}
#         self.id_count = 127
        
#         if literal_map is None:
#             self.literal_map = {}
#             self.literal_count = 157
        
#         else:
#             self.literal_map = literal_map
#             self.literal_count = int(list(self.literal_map.keys())[-1])
#             self.oov_tokens = []
    
#     def encode_tokens(self, token_list, is_train_data=True):
#         encoded_tokens = []
#         for token_type, token_value in token_list:
#             # Keyword 
#             if token_value in self.keyword_map:
#                 encoded_tokens.append(self.keyword_map[token_value])
#             # Identifier
#             elif token_type == 'IDENTIFIER':
#                 if token_value not in self.id_map:
#                     encoded_tokens.append(self.id_count)
#                     self.id_map[token_value] = self.id_count
#                     self.id_count += 1
#                 else:
#                     encoded_tokens.append(self.id_map[token_value])
#             # Literal
#             elif token_type in ['STRING_LITERAL', 'CHAR_LITERAL', 'INTEGER_LITERAL', 'FLOAT_LITERAL']:
#                 # if token_value not in self.literal_map:
#                 #     encoded_tokens.append(self.literal_count)
#                 #     self.literal_map[token_value] = self.literal_count
#                 #     self.literal_count += 1
#                 # else:
#                 #     encoded_tokens.append(self.literal_map[token_value])
#                 found = False
#                 for key, value in self.literal_map.items():
#                     if token_value == value:
#                         encoded_tokens.append(int(key))
#                         found = True
#                         break
#                 if not found:
#                     if is_train_data:
#                         encoded_tokens.append(self.literal_count)
#                         self.literal_map[self.literal_count] = token_value
#                         self.literal_count += 1
#                     else:
#                         closest_token, encoded_id = find_closest_token(self.get_vocab_map(), token_value)
#                         print(f'Find OOV token: {token_value} -> ({closest_token} - {encoded_id})')
#                         self.oov_tokens.append({
#                             "oov_token": token_value,
#                             "closest_token": closest_token,
#                             "encoded_id": encoded_id
#                         })
#                         encoded_tokens.append(encoded_id)
                            
#             # Special Character
#             elif token_type in self.special_character_map:
#                 encoded_tokens.append(self.special_character_map[token_type])
#             # undefine case
#             else:
#                 encoded_tokens.append(-1)
            
#         return encoded_tokens

#     def reset_id(self):
#         self.id_count = 127
#         self.id_map = {}
    
#     def get_literal_map(self):
#         return self.literal_map

#     def get_vocab_map(self):
#         reversed_keyword_map = {v: k for k, v in self.keyword_map.items()}
#         reversed_punctuation_and_symbol_map = {v: k for k, v in self.punctuation_and_symbol_map.items()}
#         self.vocab_map = {**reversed_keyword_map, **reversed_punctuation_and_symbol_map, **self.literal_map}
        
#         return self.vocab_map
    
#     def get_oov_tokens(self):
#         return self.oov_tokens

##################### VERSION 2 #####################
# Constants
INIT_FUNC_ID = 0
MAX_FUNC_ID = 9
INIT_VAR_ID = 10
MAX_VAR_ID = 29
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
        self.func_id = INIT_FUNC_ID
        self.func_name_map = {}
        
        # Variable: 10 - 29
        self.var_id = INIT_VAR_ID
        self.var_name_map = {}
    
    def encode_tokens(self, token_list):
        encoded_tokens = []
        for token_type, token_value in token_list:
            # Function:
            if token_type == 'FUNCTION':
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
            # Keyword 
            elif token_value in self.keyword_map:
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
            # Undefined case???
            else:
                encoded_tokens.append(-1)
        return encoded_tokens

    def reset_id(self):
        '''
        Reset current function and variable id to it initial value
        '''
        # Function: 0 - 9
        self.func_id = INIT_FUNC_ID
        self.func_name_map = {}
        
        # Variable: 10 - 29
        self.var_id = INIT_VAR_ID
        self.var_name_map = {}
        
    def get_func_id(self):
        return self.func_id
    
    def get_var_id(self):
        return self.var_id