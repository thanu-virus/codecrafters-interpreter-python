import sys
from enum import Enum
class TokenType(Enum):
    # Single-character tokens.
    LEFT_PAREN = 1
    RIGHT_PAREN = 2
    LEFT_BRACE = 3
    RIGHT_BRACE = 4
    COMMA = 5
    DOT = 6
    MINUS = 7
    PLUS = 8
    SEMICOLON = 9
    SLASH = 10
    STAR = 11
    # One or two character tokens.
    BANG = 12
    BANG_EQUAL = 13
    EQUAL = 14
    EQUAL_EQUAL = 15
    GREATER = 16
    GREATER_EQUAL = 17
    LESS = 18
    LESS_EQUAL = 19
    # Literals.
    IDENTIFIER = 20
    STRING = 21
    NUMBER = 22
    # Keywords.
    AND = 23
    CLASS = 24
    ELSE = 25
    FALSE = 26
    FUN = 27
    FOR = 28
    IF = 29
    NIL = 30
    OR = 31
    PRINT = 32
    RETURN = 33
    SUPER = 34
    THIS = 35
    TRUE = 36
    VAR = 37
    WHILE = 38
    EOF = 39
    def __str__(self):
        return super().__str__().split(".")[1]
class Token:
    def __init__(self, token_type, lexeme, literal, line):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    def __str__(self):
        return f"{self.token_type} {self.lexeme} {self.literal}"
    def __repr__(self):
        return self.__str__()
class Scanner:
    def __init__(self, source, interpreter):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.interpreter = interpreter
        self.keywords = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE,
        }
    def is_at_end(self):
        return self.current >= len(self.source)
    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", "null", self.line))
        return self.tokens
    def scan_token(self):
        c = self.advance()
        match c:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.add_token(TokenType.COMMA)
            case ".":
                self.add_token(TokenType.DOT)
            case "-":
                self.add_token(TokenType.MINUS)
            case "+":
                self.add_token(TokenType.PLUS)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case "*":
                self.add_token(TokenType.STAR)
            case "!":
                token_type = TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG
                self.add_token(token_type)
            case "=":
                token_type = (
                    TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
                )
                self.add_token(token_type)
            case "<":
                token_type = TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS
                self.add_token(token_type)
            case ">":
                token_type = (
                    TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
                )
                self.add_token(token_type)
            case "/":
                if self.match("/"):
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case " " | "\r" | "\t":
                pass
            case "\n":
                self.line += 1
            case '"':
                self.string()
            case _:
                if c.isdigit():
                    self.number()
                elif c.isalpha() or c == "_":
                    self.identifier()
                else:
                    self.interpreter.error(self.line, f"Unexpected character: {c}")
    def identifier(self):
        while self.peek().isalnum() or self.peek() == "_":
            self.advance()
        text = self.source[self.start : self.current]
        token_type = self.keywords.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type)
    def advance(self):
        self.current += 1
        return self.source[self.current - 1]
    def number(self):
        while self.peek().isdigit():
            self.advance()
        if self.peek() == "." and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()
        self.add_token(TokenType.NUMBER, float(self.source[self.start : self.current]))
    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]
    def peek(self):
        if self.is_at_end():
            return "\0"
        return self.source[self.current]
    def add_token(self, token_type, literal="null"):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))
    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        if self.is_at_end():
            self.interpreter.error(self.line, "Unterminated string.")
            return
        self.advance()
        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, value)
    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True
class LoxInterpreter:
    def __init__(self, file_contents):
        self.file_contents = file_contents
        self.had_error = False
    def run(self, tokenize, parse):
        scanner = Scanner(self.file_contents, self)
        tokens = scanner.scan_tokens()
        for token in tokens:
            if tokenize:
                print(token)
            else:
                print(token, file=sys.stderr)
        if parse:
            parser = Parser(tokens, self)
            expression = parser.expression()
            print(expression)
        if self.had_error:
            exit(65)
    def set_error(self):
        self.had_error = True
    def error(self, line_number, message):
        print(f"[line {line_number}] Error: {message}", file=sys.stderr)
        self.set_error()
class Parser:
    def __init__(self, tokens, interpreter):
        self.tokens = tokens
        self.current = 0
        self.interpreter = interpreter
    def parse(self):
        pass
    def expression(self):
        return self.equality()
    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr
    def match(self, *types):
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False
    def check(self, token_type):
        if self.is_at_end():
            return False
        return self.peek().token_type == token_type
    def is_at_end(self):
        return self.peek().token_type == TokenType.EOF
    def peek(self):
        return self.tokens[self.current]
    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()
    def previous(self):
        return self.tokens[self.current - 1]
    def comparison(self):
        expr = self.term()
        while self.match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr
    def term(self):
        expr = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr
    def factor(self):
        expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr
    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()
    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()
        self.error(self.peek(), message)
    def error(self, token, message):
        if token.token_type == TokenType.EOF:
            self.report(token.line, " at end", message)
        else:
            self.report(token.line, f" at '{token.lexeme}'", message)
    def report(self, line, where, message):
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
        self.interpreter.set_error()
        exit(65)
    def primary(self):
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NIL):
            return Literal(None)
        if self.match(TokenType.PRINT):
            return Literal("print")
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr, self.interpreter)
def Binary(left, operator, right):
    return {"left": left, "operator": operator, "right": right}
def Unary(operator, right):
    return f"({operator.lexeme} {right})"
def Literal(value):
    if value is None:
        return "nil"
    return str(value).lower()
def Grouping(expression, interpreter):
    if not expression:
        interpreter.set_error()
        return ""
    return f"(group {expression})"
def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)
    command = sys.argv[1]
    filename = sys.argv[2]
    commands = ["tokenize", "parse"]
    if command not in commands:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)
    with open(filename) as file:
        file_contents = file.read()
        interpreter = LoxInterpreter(file_contents)
        interpreter.run(command == "tokenize", command == "parse")
if __name__ == "__main__":
    main()