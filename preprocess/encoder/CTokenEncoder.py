class CTokenEncoder:
    def __init__(self):
        self.keyword_map = {
            'auto': 10, 'break': 11, 'case': 12, 'char': 13,
            'const': 14, 'continue': 15, 'default': 16, 'do': 17,
            'double': 18, 'else': 19, 'enum': 20, 'extern': 21,
            'float': 22, 'for': 23, 'goto': 24, 'if': 25,
            'int': 26, 'long': 27, 'register': 28, 'return': 29,
            'short': 30, 'signed': 31, 'sizeof': 32, 'static': 33,
            'struct': 34, 'switch': 35, 'typedef': 36, 'union': 37,
            'unsigned': 38, 'void': 39, 'volatile': 40, 'while': 41
        }
        self.special_character_map = {
            # Condition
            'QMARK': 45, 'COLON': 46, 
            # Member access
            'ARROW': 48, 'PERIOD': 49,
            # Miscellaneous
            'ESCAPE': 51, 'HASH': 52, 
            # EQUAL
            'EQUALS': 54, 
            # Arithmetic
            'PLUS': 55, 'MINUS': 56, 'TIMES': 57, 'DIVIDE': 58, 'MODULO': 59,
            # Arithmetic assignment
            'PLUSEQUAL': 60, 'MINUSEQUAL': 61, 'TIMESEQUAL': 62, 'DIVIDEEQUAL': 63, 'MODEQUAL': 64,
            # Relational 
            'EQ': 65, 'NE': 66, 'LT': 67, 'GT': 68,  'LE': 69, 'GE': 70, 
            # Increment & Decrement
            'PLUSPLUS': 71, 'MINUSMINUS': 72, 
            # Logical
            'NOT': 75, 'AND': 76, 'OR': 77, 
            # Bitwise
            'BITWISE_NOT': 80, 'BITWISE_AND': 81, 'BITWISE_OR': 82, 'BITWISE_XOR': 83, 'LSHIFT': 84, 'RSHIFT': 85, 
            # Bitwise assignment
            'ANDEQUAL': 86, 'OREQUAL': 87, 'XOREQUAL': 88, 'LSHIFTEQUAL': 89, 'RSHIFTEQUAL': 90, 
            # Separator
            'SEMICOLON': 91, 'COMMA': 92, 'LBRACKET': 93, 'RBRACKET': 94,
            'LPAREN': 96, 'RPAREN': 97, 'LBRACE': 98, 'RBRACE': 99
        }
        
        self.id_map = {}
        self.id_count = 127
        
        self.literal_map = {}
        self.literal_count = 157
    
    def encode_tokens(self, token_list):
        encoded_tokens = []
        for token_type, token_value in token_list:
            # Keyword 
            if token_value in self.keyword_map:
                encoded_tokens.append(self.keyword_map[token_value])
            # Identifier
            elif token_type == 'IDENTIFIER':
                if token_value not in self.id_map:
                    encoded_tokens.append(self.id_count)
                    self.id_map[token_value] = self.id_count
                    self.id_count += 1
                else:
                    encoded_tokens.append(self.id_map[token_value])
            # Literal
            elif token_type in ['STRING_LITERAL', 'CHAR_LITERAL', 'INTEGER_LITERAL', 'FLOAT_LITERAL']:
                if token_value not in self.literal_map:
                    encoded_tokens.append(self.literal_count)
                    self.literal_map[token_value] = self.literal_count
                    self.literal_count += 1
                else:
                    encoded_tokens.append(self.literal_map[token_value])
            # Special Character
            elif token_type in self.special_character_map:
                encoded_tokens.append(self.special_character_map[token_type])
            # undefine case
            else:
                encoded_tokens.append(-1)
            
        return encoded_tokens

    def get_id_map(self):
        return self.id_map

    def get_literal_map(self):
        return self.literal_map