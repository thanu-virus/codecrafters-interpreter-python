import sys

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)
        
    command = sys.argv[1]
    filename = sys.argv[2]
    
    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)
    
    try:
        with open(filename) as file:
            file_contents = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.", file=sys.stderr)
        exit(1)

    exit_code = 0
    toks = []
    errs = []
    
    if file_contents:
        line_no = 1
        ptr = 0
        length = len(file_contents)
        string=""
        chh=""
        
        single_char_tokens = {
            '(': "LEFT_PAREN", ')': "RIGHT_PAREN",
            '{': "LEFT_BRACE", '}': "RIGHT_BRACE",
            ',': "COMMA", '.': "DOT", 
            '+': "PLUS", '-': "MINUS", 
            ';': "SEMICOLON", '*': "STAR", 
            '/': "SLASH",
        }
        
        multi_char_tokens = {
            '=': ("EQUAL", "EQUAL_EQUAL", "="),
            '!': ("BANG", "BANG_EQUAL", "="),
            '<': ("LESS", "LESS_EQUAL", "="),
            '>': ("GREATER", "GREATER_EQUAL", "="),
        }
        
        while ptr < length:
            ch = file_contents[ptr]
            if ch in single_char_tokens:
                if ch == '/' and ptr < length - 1 and file_contents[ptr + 1] == '/':
                    # Skip to the end of the line for a comment
                    while ptr < length and file_contents[ptr] != "\n":
                        ptr += 1
                    continue
                else:
                    toks.append(f"{single_char_tokens[ch]} {ch} null")
            elif ch in multi_char_tokens:
                base_name, combined_name, next_char = multi_char_tokens[ch]
                if ptr < length - 1 and file_contents[ptr + 1] == next_char:
                    toks.append(f"{combined_name} {ch}{next_char} null")
                    ptr += 1
                else:
                    toks.append(f"{base_name} {ch} null")
            elif ch == '\n':
                line_no += 1
            elif ch in " \r\t":
                pass  # Skip whitespace
            elif ch == '"':
                ptr+=1
                word = ""
                while ptr < length and file_contents[ptr] != '"':
                    word += file_contents[ptr]
                    ptr += 1
                if ptr == length:
                    error = True
                    print(f"[line {line_no}] Error: Unterminated string.", file=sys.stderr)
                    exit_code=65
                else:
                    toks.append(f'STRING "{word}" {word}')
            else:
                errs.append(f"[line {line_no}] Error: Unexpected character: {ch}")
                exit_code = 65
            ptr += 1
        
        toks.append("EOF  null")  # End of file token
        
        if errs:
            print("\n".join(errs), file=sys.stderr)
        print("\n".join(toks))
    else:
        print("EOF null")  # If the file is empty, just print EOF
    
    exit(exit_code)

if __name__ == "__main__":
    main()
