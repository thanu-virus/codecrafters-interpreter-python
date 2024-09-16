import sys
def main():
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
    if file_contents:
        # Placeholder, remove this line when implementing the scanner
        for c in file_contents:
            if c == "(":
                print("LEFT_PAREN ( null")
            if c == ")":
                print("RIGHT_PAREN ) null")
            if c == "{":
                print("LEFT_BRACE { null")
            if c == "}":
                print("RIGHT_BRACE } null")
            if c == ",":
                print("COMMA , null")
            if c == ".":
                print("DOT .null")
            if c == "-":
                print(" MINUS - null")
            if c == "+":
                print(" PLUS + null")
            if c == ";":
                print("SEMI-COLON ; null")
            if c == "*":
                print("STAR * null")
            if c == "/":
                print(" SLASH / null")
        print("EOF  null")
    else:
        print("EOF  null")
if __name__ == "__main__":
    main()
