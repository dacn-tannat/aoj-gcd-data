### Original:

```bash
{
    "judge_id": 9596717,
    "source_code": "int main()\n{\n    int x, y;\n    scanf(\"%d %d\", &x, &y);\n\n    int gcd;\n    while (y != 0)\n    {\n        gcd = x % y;\n        x = y;\n        y = gcd;\n        //printf(\"x:%d,y:%d\n\", x, y);\n    }\n    printf(\"%d\n\", x);\n}\n",
    "status": 4,
    "raw_tokens": [ "int", "main", "(", ")", "{", "int", "x", ",", "y", ";", "scanf", "(", "\"%d %d\"", ",", "&", "x", ",", "&", "y", ")", ";", "int", "gcd", ";", "while", "(", "y", "!=", 0, ")", "{", "gcd", "=", "x", "%", "y", ";", "x", "=", "y", ";", "y", "=", "gcd", ";", ",", "x", ",", "y", ")", ";", "}", "printf", "(", "%", "d", ",", "x", ")", ";", "}"
    ],
}
```

```c
int main()
{
    int x, y;
    scanf(\"%d %d\", &x, &y);

    int gcd;
    while (y != 0)
    {
        gcd = x % y;
        x = y;
        y = gcd;
        //printf(\"x:%d,y:%d\n\", x, y);
    }
    printf(\"%d\n\", x);
}

```

### Expected:

```bash
{
    "judge_id": 9596717,
    "source_code": "int main()\n{\n    int x, y;\n    scanf(\"%d %d\", &x, &y);\n\n    int gcd;\n    while (y != 0)\n    {\n        gcd = x + y;\n        x = y;\n        y = gcd;\n        //printf(\"x:%d,y:%d\\n\", x, y);\n    }\n    printf(\"%f\\n\", x);\n}\n",
    "status": 4,
    "raw_tokens": [ "int", "main", "(", ")", "{", "int", "x", ",", "y", ";", "scanf", "(", "\"%d %d\"", ",", "&", "x", ",", "&", "y", ")", ";", "int", "gcd", ";", "while", "(", "y", "!=", "0", ")", "{", "gcd", "=", "x", "+", "y", ";", "x", "=", "y", ";", "y", "=", "gcd", ";", "}", "printf", "(", "%", "f", ",", "x", ")", ";", "}"
    ],
    "bug_positions": [
        {
            "line": 7,
            "token_location": 35,
            "original_token": "%",
            "error_token": "+"
        },
        {
            "line": 11,
            "token_location": 50,
            "original_token": "d",
            "error_token": "f",
        }
    ]
}
```

```c
int main()
{
    int x, y;
    scanf(\"%d %d\", &x, &y);
    int gcd;
    while (y != 0)
    {
        gcd = x + y; // line 7, token 35, '%' -> '+'
        x = y;
        y = gcd;
        //printf(\"x:%d,y:%d\\n\", x, y);
    }
    printf(\"%f\\n\", x); // line 11, token 50, 'd' -> 'f'
}

```
