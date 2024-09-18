from typing import Any, Dict, List
from app.error import error
from app.token import Token, TokenType
class Scanner:
    start: int
    current: int
    line: int
    tokens: List[Token]
    def __init__(self, source: str):
        self.source = source
        self.start = 0
        self.current = 0
        self.line = 1
        self.tokens = []
    def advance(self) -> str | None:
        try:
            idx = self.current
            self.current += 1
            return self.source[idx]
        except IndexError:
            return None
    def peek(self) -> str | None:
    def peek(self, offset: int = 0) -> str:
        try:
            return self.source[self.current]
            return self.source[self.current + offset]
        except IndexError:
            return None
            return "\0"
    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens
    def is_at_end(self) -> bool:
        return self.current >= len(self.source)
    def add_token(self, type: TokenType, literal: Any = None):
        a, b = self.start, self.current
        text = self.source[a:b]
        token = Token(type, text, literal, self.line)
        self.tokens.append(token)
    def cmp(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.peek() != expected:
            return False
        self.current += 1
        return True
    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        if self.is_at_end():
            error(self.line, "Unterminated string.")
            return
        self.advance()
        a, b = self.start + 1, self.current - 1
        value = self.source[a:b]
        self.add_token(TokenType.STRING, value)
    def number(self):
        while self.peek().isnumeric():
            self.advance()
        if self.peek() == "." and self.peek(1).isnumeric():
            self.advance()
            while self.peek().isnumeric():
                self.advance()
        a, b = self.start, self.current
        self.add_token(TokenType.NUMBER, float(self.source[a:b]))
    def scan_token(self):
        c = self.advance()
        match c:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
                pass
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
                pass
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
                pass
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
                pass
            case ",":
                self.add_token(TokenType.COMMA)
                pass
            case ".":
                self.add_token(TokenType.DOT)
                pass
            case "-":
                self.add_token(TokenType.MINUS)
                pass
            case "+":
                self.add_token(TokenType.PLUS)
                pass
            case ";":
                self.add_token(TokenType.SEMICOLON)
                pass
            case "*":
                self.add_token(TokenType.STAR)
                pass
            case "!":
                self.add_token(
                    TokenType.BANG_EQUAL if self.cmp("=") else TokenType.BANG
                )
                pass
            case "=":
                self.add_token(
                    TokenType.EQUAL_EQUAL if self.cmp("=") else TokenType.EQUAL
                )
                pass
            case "<":
                self.add_token(
                    TokenType.LESS_EQUAL if self.cmp("=") else TokenType.LESS
                )
                pass
            case ">":
                self.add_token(
                    TokenType.GREATER_EQUAL if self.cmp("=") else TokenType.GREATER
                )
                pass
            case "/":
                if self.cmp("/"):
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
                pass
            case " ":
                pass
            case "\r":
                pass
            case "\t":
                pass
            case "\n":
                self.line += 1
                pass
            case '"':
                self.string()
                pass
            case _:
                error(self.line, f"Unexpected character: {c}")
                if c and c.isnumeric():
                    self.number()
                else:
                    error(self.line, f"Unexpected character: {c}")
                pass
    if error:
        exit(65)
if __name__ == "__main__":
    main()