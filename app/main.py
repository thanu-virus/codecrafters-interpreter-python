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
        error=False
        for c in file_contents:
            if c == "(":
                print("LEFT_PAREN ( null")
            elif c == ")":
                print("RIGHT_PAREN ) null")
            elif c == "{":
                print("LEFT_BRACE { null")
            elif c == "}":
                print("RIGHT_BRACE } null")
            elif c == ",":
                print("COMMA , null")
            elif c == ".":
                print("DOT . null")
            elif c == "-":
                print("MINUS - null")
            elif c == "+":
                print("PLUS + null")
            elif c == ";":
                print("SEMI-COLON ; null")
            elif c == "*":
                print("STAR * null")
            elif c == "/":
                print("SLASH / null")
            else:
                error=True
                line_number=file_contents.count("\n",0,file_contents.find(c))+1
                print("[line %s] Error: Unexpected charecter: %s"%(line_number,c),file=sys.stderr,)                
        print("EOF  null")
        if error==True:
            exit(65)
        else:
            exit(0)
if __name__ == "__main__":
    main()
