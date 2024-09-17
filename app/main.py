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
    
    with open(filename) as file:
        file_contents = file.read()
    
    exit_code = 0
    toks = []
    errs = []
    
    if file_contents:
        line_no = 1
        ptr = 0
        
        while ptr < len(file_contents):
            ch = file_contents[ptr]
            ch_name = ""
            
            if ch == "(":
                ch_name = "LEFT_PAREN"
                ptr += 1
            elif ch == ")":
                ch_name = "RIGHT_PAREN"
                ptr += 1
            elif ch == "{":
                ch_name = "LEFT_BRACE"
                ptr += 1
            elif ch == "}":
                ch_name = "RIGHT_BRACE"
                ptr += 1
            elif ch == ",":
                ch_name = "COMMA"
                ptr += 1
            elif ch == ".":
                ch_name = "DOT"
                ptr += 1
            elif ch == "+":
                ch_name = "PLUS"
                ptr += 1
            elif ch == "-":
                ch_name = "MINUS"
                ptr += 1
            elif ch == ";":
                ch_name = "SEMICOLON"
                ptr += 1
            elif ch == "*":
                ch_name = "STAR"
                ptr += 1
            elif ch == "\n":
                line_no += 1
                ptr += 1
                continue
            elif ch == "=":
                if ptr < len(file_contents) - 1 and file_contents[ptr + 1] == "=":
                    ch_name = "EQUAL_EQUAL"
                    ch = "=="
                    ptr += 2
                else:
                    ch_name = "EQUAL"
                    ptr += 1
            elif ch == "!":
                if ptr < len(file_contents) - 1 and file_contents[ptr + 1] == "=":
                    ch_name = "BANG_EQUAL"
                    ch = "!="
                    ptr += 2
                else:
                    ch_name = "BANG"
                    ptr += 1
            elif ch == "<":
                if ptr < len(file_contents) - 1 and file_contents[ptr + 1] == "=":
                    ch_name = "LESS_EQUAL"
                    ch = "<="
                    ptr += 2
                else:
                    ch_name = "LESS"
                    ptr += 1
            elif ch == ">":
                if ptr < len(file_contents) - 1 and file_contents[ptr + 1] == "=":
                    ch_name = "GREATER_EQUAL"
                    ch = ">="
                    ptr += 2
                else:
                    ch_name = "GREATER"
                    ptr += 1
            
            else:
                errs.append(f"[line {line_no}] Error: Unexpected character: {ch}")
                exit_code = 65
                ptr += 1
                continue  # Skip adding this character to toks
            
            if ch_name:
                toks.append(f"{ch_name} {ch} null")
        
        toks.append("EOF  null")  # Placeholder, remove this line when implementing the scanner
        print("\n".join(errs), file=sys.stderr)
        print("\n".join(toks))
    else:
        print("EOF  null")  # Placeholder, remove this line when implementing the scanner
    
    exit(exit_code)

if __name__ == "__main__":
    main()
