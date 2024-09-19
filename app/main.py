import enum
import pathlib
import sys
from typing import Any

# Define token types using an Enum
class TokenType(enum.Enum):
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    LEFT_BRACE = "LEFT_BRACE"
    RIGHT_BRACE = "RIGHT_BRACE"
    STAR = "STAR"
    DOT = "DOT"
    COMMA = "COMMA"
    PLUS = "PLUS"
    MINUS = "MINUS"
    SEMICOLON = "SEMICOLON"
    EQUAL = "EQUAL"
    EQUAL_EQUAL = "EQUAL_EQUAL"
    BANG = "BANG"
    BANG_EQUAL = "BANG_EQUAL"
    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"
    SLASH = "SLASH"
    STRING = "STRING"
    NUMBER = "NUMBER"
    IDENTIFIER="IDENTIFIER"
    EOF = "EOF"


# Define a Token class to represent individual tokens
class Token:
    def __init__(self, type: TokenType, lexeme: str, literal: Any | None, line: int) -> None:
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self) -> str:
        literal_str = "null" if self.literal is None else str(self.literal)
        return f"{self.type.value} {self.lexeme} {literal_str}"

# Scanner class to tokenize the source code
class Scanner:
    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens: list[Token] = []  # List to store generated tokens
        self.start = 0  # Start of the current lexeme
        self.current = 0  # Current character position in the source
        self.line = 1  # Track line numbers for error reporting
        self.errors: list[str] = []  # List to store error messages

    def scan_tokens(self) -> tuple[list[Token], list[str]]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens, self.errors

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_token(self) -> None:
        char = self.advance()
        match char:
            case "(": self.add_token(TokenType.LEFT_PAREN)
            case ")": self.add_token(TokenType.RIGHT_PAREN)
            case "{": self.add_token(TokenType.LEFT_BRACE)
            case "}": self.add_token(TokenType.RIGHT_BRACE)
            case "*": self.add_token(TokenType.STAR)
            case ".": self.add_token(TokenType.DOT)
            case ",": self.add_token(TokenType.COMMA)
            case "+": self.add_token(TokenType.PLUS)
            case "-": self.add_token(TokenType.MINUS)
            case ";": self.add_token(TokenType.SEMICOLON)
            case "!":
                # Handle '!=' or '!'
                self.add_token(TokenType.BANG_EQUAL) if self.match("=") else self.add_token(TokenType.BANG)
            case "=":
                # Handle '==' or '='
                self.add_token(TokenType.EQUAL_EQUAL) if self.match("=") else self.add_token(TokenType.EQUAL)
            case "<":
                # Handle '<=' or '<'
                self.add_token(TokenType.LESS_EQUAL) if self.match("=") else self.add_token(TokenType.LESS)
            case ">":
                # Handle '>=' or '>'
                self.add_token(TokenType.GREATER_EQUAL) if self.match("=") else self.add_token(TokenType.GREATER)
            case "/":
                # Handle comments or '/'
                if self.match("/"):
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case " " | "\r" | "\t":
                # Ignore whitespace
                ...
            case "\n":
                # New line, increment line number
                self.line += 1
            case '"':
                # Handle string literals
                self.string()
            case _:
                # Handle numbers or errors
                if self.is_digit(char):
                    self.number()
                elif self.is_alpha_numeric(char):
                    self.identifier()
                else:
                    self.error(f"Unexpected character: {char}")

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, type: TokenType, literal: Any | None = None) -> None:
        text = self.source[self.start: self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def peek(self) -> str:
        return "\0" if self.is_at_end() else self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def string(self) -> None:
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        if self.is_at_end():
            self.errors.append(f"[line {self.line}] Error: Unterminated string.")
            return
        self.advance()  # Consume the closing "
        value = self.source[self.start + 1: self.current - 1]
        self.add_token(TokenType.STRING, value)

    def is_digit(self, char: str) -> bool:
        return char >= "0" and char <= "9"

    def number(self) -> None:
        # Handle integer and floating point numbers
        while self.is_digit(self.peek()):
            self.advance()
        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()  # Consume the '.'
            while self.is_digit(self.peek()):
                self.advance()
        value = float(self.source[self.start: self.current])
        self.add_token(TokenType.NUMBER, value)

    def is_alpha(self, char: str) -> bool:
        return char >= "a" and char <= "z" or char >= "A" and char <= "Z" or char == "_"
    def is_alpha_numeric(self, char: str) -> bool:
        return self.is_alpha(char) or self.is_digit(char)
    def identifier(self) -> None:
        reserved_keywords={
          "and": AND, "class":CLASS, "else":ELSE, "false":FALSE, "for":FOR , "fun":FUN, "if":IF, "nil":NIL, "or":OR, "print":PRINT, "return":RETURN, "super":SUPER, "this":THIS "true":TRUE, "var":VAR, "while":WHILE  
        }
        while self.is_alpha_numeric(self.peek()):
            self.advance()
        text = self.source[self.start: self.current]
        if text in reserved_keywords:
            print(f"{reserved_keywords.text} {text} null")
        else:
        self.add_token(TokenType.IDENTIFIER)
    def error(self, char: str) -> None:
        self.errors.append(f"[line {self.line}] Error: {char}")

# Main function to run the scanner
def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    # Read file content
    file_contents = pathlib.Path(filename).read_text()

    # Initialize scanner and scan tokens
    scanner = Scanner(file_contents)
    tokens, errors = scanner.scan_tokens()

    # Print tokens
    for token in tokens:
        print(token)

    # Print errors, if any
    for error in errors:
        print(error, file=sys.stderr)

    # Exit with error code if there are any errors
    if errors:
        exit(65)

if __name__ == "__main__":
    main()
