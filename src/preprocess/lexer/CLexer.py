import ply.lex as lex

class CLexer:
    """
    A lexer for the C programming language.

    This class uses the PLY (Python Lex-Yacc) library to tokenize C code.
    It defines token types, their associated regular expressions, and methods
    for handling different types of tokens.
    """

    def __init__(self):
        """
        Initialize the CLexer.

        This method creates a lexer object and initializes a set to store any
        encountered error characters.
        """
        self.lexer = lex.lex(module=self)
        self.error_characters = set()
        
    def tokenize(self, input_string):
        """
        Tokenize the input string.

        Args:
            input_string (str): The C code to tokenize.

        Returns:
            list: A list of tuples, where each tuple contains (token_type, token_value).
        """
        self.lexer.input(input_string)
        tokens_list = []
        while True:
            tok = self.lexer.token()
            if not tok: 
                break
            tokens_list.append(tok)
        return [(token.type, token.value) for token in tokens_list]

    def get_error_characters(self):
        """
        Get the set of error characters encountered during tokenization.

        Returns:
            set: A set of characters that were not recognized by the lexer.
        """
        return self.error_characters

    # Token list
    tokens = [
        'IDENTIFIER', 'INTEGER_LITERAL', 'FLOAT_LITERAL', 'STRING_LITERAL', 'CHAR_LITERAL',
        # Arithmetic operators: [+ - * / %]
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO', 
        # Bitwise operators: [& | ^ ~ << >>]
        'BITWISE_AND', 'BITWISE_OR', 'BITWISE_XOR', 'BITWISE_NOT', 'LSHIFT', 'RSHIFT', 
        # Assignment operators: =
        'EQUALS',
        # Arithmetic assignment operators: [+= -= *= /= %=]
        'PLUSEQUAL', 'MINUSEQUAL', 'TIMESEQUAL', 'DIVIDEEQUAL', 'MODEQUAL',
        # Bitwise assignment operators: [&= |= ^= <<= >>=]
        'ANDEQUAL', 'OREQUAL', 'XOREQUAL', 'LSHIFTEQUAL', 'RSHIFTEQUAL',
        # Logical operators: [&& || !]
        'AND', 'OR', 'NOT', 
        # Relational operators: [== != < > <= >=]
        'EQ', 'NE', 'LT', 'GT', 'LE', 'GE', 
        # Increment and Decrement operators: [++ --]
        'PLUSPLUS', 'MINUSMINUS',
        # Conditional operator: [? :]
        'QMARK', 'COLON',
        # Member access operator: [->, .]
        'ARROW', 'PERIOD',
        # Miscellaneous operators: [# \]
        'HASH', 'ESCAPE',
        # Separators: [; , [ ] ( ) { }]
        'SEMICOLON', 'COMMA', 'LBRACKET', 'RBRACKET', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
        # Comment
        'COMMENT_MULTI', 'COMMENT_SINGLE'
    ] + [
        # keywords
        'AUTO', 'BREAK', 'CASE', 'CHAR', 'CONST', 'CONTINUE', 'DEFAULT', 'DO',
        'DOUBLE', 'ELSE', 'ENUM', 'EXTERN', 'FLOAT', 'FOR', 'GOTO', 'IF',
        'INT', 'LONG', 'REGISTER', 'RETURN', 'SHORT', 'SIGNED', 'SIZEOF', 
        'STATIC', 'STRUCT', 'SWITCH', 'TYPEDEF', 'UNION', 'UNSIGNED', 'VOID', 
        'VOLATILE', 'WHILE'
    ]

    # Regular expressions for tokens
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_MODULO = r'%'

    t_EQUALS = r'='
    t_PLUSEQUAL = r'\+='
    t_MINUSEQUAL = r'-='
    t_TIMESEQUAL = r'\*='
    t_DIVIDEEQUAL = r'/='
    t_MODEQUAL = r'%='
    t_ANDEQUAL = r'&='
    t_OREQUAL = r'\|='
    t_XOREQUAL = r'\^='
    t_LSHIFTEQUAL = r'<<='
    t_RSHIFTEQUAL = r'>>='

    t_EQ = r'=='
    t_NE = r'!='
    t_LT = r'<'
    t_GT = r'>'
    t_LE = r'<='
    t_GE = r'>='

    t_AND = r'&&'
    t_OR = r'\|\|'
    t_NOT = r'!'

    t_BITWISE_AND = r'&'
    t_BITWISE_OR = r'\|'
    t_BITWISE_XOR = r'\^'
    t_BITWISE_NOT = r'~'
    t_LSHIFT = r'<<'
    t_RSHIFT = r'>>'

    t_PLUSPLUS = r'\+\+'
    t_MINUSMINUS = r'--'
    
    t_PERIOD = r'\.'
    t_ARROW = r'->'
    
    t_SEMICOLON = r';'
    t_COMMA = r','
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    
    t_COLON = r':'
    t_QMARK = r'\?'
    
    t_HASH = r'\#'
    t_ESCAPE = r'\\'
    
    # Ignore spaces, tabs, and newlines
    t_ignore = ' \t'

    # Comments
    def t_COMMENT_SINGLE(self, t):
        r'//.*'
        pass

    def t_COMMENT_MULTI(self, t):
        r'/\*[\s\S]*?\*/'
        t.lexer.lineno += t.value.count('\n')
        pass

    # Keyword map
    keyword_map = {
        'auto': 'AUTO', 'break': 'BREAK', 'case': 'CASE', 'char': 'CHAR',
        'const': 'CONST', 'continue': 'CONTINUE', 'default': 'DEFAULT', 'do': 'DO',
        'double': 'DOUBLE', 'else': 'ELSE', 'enum': 'ENUM', 'extern': 'EXTERN',
        'float': 'FLOAT', 'for': 'FOR', 'goto': 'GOTO', 'if': 'IF',
        'int': 'INT', 'long': 'LONG', 'register': 'REGISTER', 'return': 'RETURN',
        'short': 'SHORT', 'signed': 'SIGNED', 'sizeof': 'SIZEOF', 'static': 'STATIC',
        'struct': 'STRUCT', 'switch': 'SWITCH', 'typedef': 'TYPEDEF', 'union': 'UNION',
        'unsigned': 'UNSIGNED', 'void': 'VOID', 'volatile': 'VOLATILE', 'while': 'WHILE'
    }

    def t_IDENTIFIER(self, t):
        r'[A-Za-z_][A-Za-z0-9_]*'
        t.type = self.keyword_map.get(t.value, 'IDENTIFIER')  # Check for keywords
        return t

    def t_STRING_LITERAL(self, t):
        r'\"([^\\\n]|(\\.))*?\"'
        return t

    def t_CHAR_LITERAL(self, t):
        r'\'([^\\\n]|(\\.))*?\''
        return t

    def t_FLOAT_LITERAL(self, t):
        r'(\d+\.\d*|\.\d+|\d+[eE][+-]?\d+)'
        t.value = float(t.value)
        return t

    def t_INTEGER_LITERAL(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        """
        Error handling method for the lexer.

        This method is called when the lexer encounters an illegal character.
        It prints an error message, adds the character to the error_characters set,
        and skips the character.

        Args:
            t: The token object representing the illegal character.
        """
        print(f"Illegal character '{t.value[0]}'")
        self.error_characters.add(t.value[0])
        t.lexer.skip(1)
