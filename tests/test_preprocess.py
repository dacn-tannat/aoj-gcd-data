from preprocess import *

mocked_data = [
    {
        "judge_id": 910025,
        "sourceCode": "#include <stdio.h>\n\nmain()\n{\n  int a;\n  int b;\n  scanf(\"%d %d\",&a,&b);\n  if(a < b){\n    a = a + b;\n    b = a - b;\n    a = a - b;\n  }\n  int c;\n  while(b != 0)\n    {\n      c = a % b;\n      a = b;\n      b = c;\n    }\n  printf(\"%d\\n\",a);\n  return 0;\n}\n",
        "status": 4
    },
    {
        "judge_id": 910006,
        "sourceCode": "#include <stdio.h>\n\nmain()\n{\n  int a;\n  int b;\n  scanf(\"%d %d\",&a,&b);\n  if(a < b){\n    a = a + b;\n    b = a - b;\n    a = a - b;\n  }\n  int c;\n  while(b != 0)\n    {\n      c = a % b;\n      a = b;\n      b = c;\n    }\n  printf(\"%d\\n\",a);\n}\n",
        "status": 7
    },
    {
        "judge_id": 123,
        "sourceCode": "#include <stdio.h>\n\n// Function to compute the greatest common divisor (GCD)\nint gcd(int a, int b) {\n    while (b != 0) {\n        int temp = b;\n        b = a % b;\n        a = temp;\n    }\n    return a;\n}\n\nint main() {\n    int a, b;\n    scanf(\"%d %d\", &a, &b);\n\n    int result = gcd(a, b);\n    printf(\"%d\\n\", result);\n\n    return 0;\n}\n\n",
        "status": 4
    }
]

def test_tokenize_and_encode():
    processed_data = tokenize_and_encode(mocked_data)
    for data in processed_data:
        for i in range(len(data['raw_tokens'])):
            print(f'{i}\t{data["raw_tokens"][i]}\t{data["encoded_tokens"][i]}')
        print('------------------------------------------------')
            
test_tokenize_and_encode()