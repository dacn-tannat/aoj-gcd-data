from .lexer.CLexer import CLexer

def detect_line_of_bug_location(src_obj):
    bugs = src_obj.get('bug_positions', [])
    # Check if current source code has bug
    if len(bugs) > 0:
        src = src_obj.get("source_code", "")
        lines = src.split('\n')
        lexer = CLexer()
        
        token_count = 0
        line_token_info = []
        
        # Loop through each line and tokenize that line -> number of tokens of each line
        for index, line in enumerate(lines):
            tokens = lexer.tokenize(line)
            num_tokens = len(tokens)
            
            # Tracking each line start and end location of token in 'raw_tokens' list
            line_token_info.append({
                "line_number": index,
                "token_start_index": token_count if num_tokens > 0 else -1,
                "token_end_index": token_count + num_tokens - 1 if num_tokens > 0 else -1,
            })
            
            token_count += num_tokens

        # Loop through each bug in source code
        for bug in bugs:
            bug_token_index = bug.get('token_location')
            
            for line_info in line_token_info:
                start_index = line_info["token_start_index"]
                end_index = line_info["token_end_index"]
                
                # Check if this bug is belong to current line
                if start_index <= bug_token_index <= end_index:
                    bug["line_number"] = line_info["line_number"] + 1
                    break

    return src_obj

def label_line_for_bug(data):
    line_processed_metrics_data = []
    for src_obj in data:
        src_obj_with_line = detect_line_of_bug_location(src_obj)
        line_processed_metrics_data.append(src_obj_with_line)
    return line_processed_metrics_data
        
    
