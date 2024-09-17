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
    # Uncomment this block to pass the first stage
    toks = []
    errs = []
    if file_contents:
        line_no = 1
        for c in file_contents:
            ptr = 0
            while ptr < len(file_contents):
                c = file_contents[ptr]
                c_name = ""
                if c == "(":
                    c_name = "LEFT_PAREN"
                elif ch == ")":
                    c_name = "RIGHT_PAREN"
                elif c == "{":
                    c_name = "LEFT_BRACE"
                elif c == "}":
                    c_name = "RIGHT_BRACE"
                elif c == ",":
                    c_name = "COMMA"
                elif c == ".":
                    c_name = "DOT"
                elif c == "+":
                    c_name = "PLUS"
                elif c == "-":
                    c_name = "MINUS"
                elif c == ";":
                    c_name = "SEMICOLON"
                elif c == "*":
                    c_name = "STAR"
                elif c == "\n":
                    line_no += 1
                    continue
                elif c == "=":
                    if ptr < len(file_contents) - 1 and file_contents[ptr + 1] == "=":
                        c_name = "EQUAL_EQUAL"
                        c = "=="
                    else:
                        c_name = "EQUAL"
                else:
                    errs.append(f"[line {line_no}] Error: Unexpected character: {ch}")
                    exit_code = 65
                    ptr += 1
                    continue
                ptr += len(c)
                toks.append(f"{c_name} {c} null")
        toks.append(
                "EOF  null"
            )  # Placeholder, remove this line when implementing the scanner
        print("\n".join(errs), file=sys.stderr)
        print("\n".join(toks))
    else:
            print(
                "EOF  null"
            )  # Placeholder, remove this line when implementing the scanner
    exit(exit_code)
if __name__ == "__main__":
    main()