'''
To run this file: python3 -m tests.test_token
'''

from preprocess import *

str1 = '''
// This is a comment 
int main() {
    if (a > b) {
        /* 
        Hehe Duy Anh ngu nhu con cho
        Duy Anh oc cho 
        Duy Anh loz
        Multiple line comment
        */
        int a = 1; // Hehe comment tao lao
    }
}
'''

str2 = '#include <stdio.h>\n\n// Function to compute the greatest common divisor (GCD)\nint gcd(int a, int b) {\n    while (b != 0) {\n        int temp = b;\n        b = a % b;\n        a = temp;\n    }\n    return a;\n}\n\nint main() {\n    int a, b;\n    scanf(\"%d %d\", &a, &b);\n\n    int result = gcd(a, b);\n    printf(\"%d\\n\", result);\n\n    return 0;\n}\n\n'

str3 = '#include <stdio.h>\n\nint gcd(int x, int y){\n    int tmp;\n    if (x < y){\n        tmp = x;\n        x = y;\n        y = tmp;\n    }\n    int r;\n    while (y > 0){\n        r = x % y;\n        x = y;\n        y = r;\n    }\n    \n    return x;\n}\n\nint main(void){\n    int A, B;\n    scanf(\"%d %d\", &A, &B);\n    //printf(\"%d %d\", A, B);\n    \n    printf(\"%d\", gcd(A, B));\n    return 0;\n    \n}\n'

str4 = '#include <stdio.h>\n#include <math.h>\n\nint main()\n{\n  int n, count;\n\n  scanf(\"%d\", &n); // read the size of array\n\n  int arr[n];\n\n  for (int i = 0; i < n; i++)\n  {\n    scanf(\"%d\", &arr[i]); // get each element of array one by one\n  }\n\n  for (int i = 0; i < n; i++)\n  {\n    if (isPrime(arr[i]) == 1)\n      count++;\n  }\n\n  printf(\"%d\n\", count);\n\n  return 0;\n}\n\nint isPrime(int n)\n{\n  for (int i = 2; i < sqrt(n); i++)\n  {\n    if (n % i == 0)\n      return 0;\n  }\n  return 1;\n}\n'

str5 = '#include <stdio.h>\n\nint gcd(int,int);\nvoid swap(int*,int*);\n\nint main()\n {\n    int x,y,i,n;\n    scanf(\"%d%d\",&x,&y);\n    if (x<y)\n        {\n            swap(&x,&y);\n        }\n\n        //gcd(x,y);\n\n    \n    printf(\"%d\n\",gcd(x,y));\n\n    return 0;   \n}\nvoid swap(int*x,int*y)\n{\n    int temp;\n    temp=*x;\n    *x=*y;\n    *y=temp;\n    return;\n}\nint gcd (int x,int y)\n{\n    \n    int n,i;\n   //n=y;\n\n            /*if(x%i==0&&y%i==0)\n            {\n                return i;\n            }*/ \n\n        while(y>0)\n        {\n            n=x%y;\n            x=y;\n            y=n;\n        }\n            return x;\n        \n       \n        \n       \n    \n    return 1;\n\n}\n\n\n\n'

# str2
# Input: 
# #include <stdio.h>
# // Function to compute the greatest common divisor (GCD)
# int gcd(int a, int b) {
#   while (b != 0) {        
#       int temp = b;
#       b = a % b;
#       a = temp;
#   }
#   return a;
# }
# 
# int main() {
#   int a, b;
#   scanf(\"%d %d\", &a, &b);
# 
#   int result = gcd(a, b);
#   printf(\"%d\\n\", result);
#   return 0;
# }
#
# 
# Output:
# '#', 'include', '<', 'stdio', '.', 'h', '>', 'int', 'gcd', '(', 'int', 'a', ',', 'int', 'b', ')', '{', 
# 'while', '(', 'b', '!=', 0, ')', '{', 'int', 'temp', '=', 'b', ';', 'b', '=', 'a', '%', 'b', ';', 'a', 
# '=', 'temp', ';', '}', 'return', 'a', ';', '}', 'int', 'main', '(', ')', '{', 'int', 'a', ',', 'b', ';', 
# 'scanf', '(', '"%d %d"', ',', '&', 'a', ',', '&', 'b', ')', ';', 'int', 'result', '=', 'gcd', '(', 'a', ',', 'b', ')', ';', 
# 'printf', '(', '"%d\\n"', ',', 'result', ')', ';', 'return', 0, ';', '}'

def test_lexer():
    # input_string = "if (a > b) {a = b;} else {a = c;}"
    input_string = str5
    lexer = CLexer()
    
    tokens = lexer.tokenize(input_string)
    toks = [token[1] for token in tokens]
    print(toks)

def test_lexer_and_encoder():
    input_string = "if (a > b) {a = b;} else {a = c;}"
    lexer = CLexer()
    tokens = lexer.tokenize(input_string)

    encoder = CTokenEncoder()
    encoded_tokens = encoder.encode_tokens(tokens)
    
    for i in range(len(tokens)):
        print(f'{i}\t{tokens[i][1]}\t{encoded_tokens[i]}')

test_lexer()