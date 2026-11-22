from apidsl.errors import CompileError, ErrorKind
from apidsl.tokens import KEYWORDS, SYMBOLS, Token, TokenType

ESCAPES = {'"': '"', "\\": "\\", "n": "\n", "t": "\t"}
WHITESPACE = " \t\r\n"


def is_digit(char: str) -> bool:
    return "0" <= char <= "9"


def is_ident_start(char: str) -> bool:
    return char == "_" or ("a" <= char <= "z") or ("A" <= char <= "Z")


def is_ident_part(char: str) -> bool:
    return is_ident_start(char) or is_digit(char)


class Lexer:
    def __init__(self, source: str) -> None:
        self._source = source
        self._pos = 0
        self._line = 1
        self._col = 1

    def tokenize(self) -> list[Token]:
        tokens = []
        while True:
            self._skip_whitespace_and_comments()
            if self._at_end():
                tokens.append(Token(TokenType.EOF, "", None, self._line, self._col))
                return tokens
            tokens.append(self._next_token())

    def _next_token(self) -> Token:
        line, col, start = self._line, self._col, self._pos
        char = self._peek()
        if char == '"':
            return self._string(line, col, start)
        if is_digit(char) or (char == "-" and is_digit(self._peek(1))):
            return self._number(line, col, start)
        if is_ident_start(char):
            return self._word(line, col, start)
        return self._symbol(line, col)

    def _string(self, line: int, col: int, start: int) -> Token:
        self._advance()
        chars = []
        while True:
            if self._at_end() or self._peek() == "\n":
                raise self._error("unterminated string", line, col)
            if self._peek() == '"':
                self._advance()
                break
            if self._peek() == "\\":
                chars.append(self._escape(line, col))
            else:
                chars.append(self._advance())
        return Token(TokenType.STRING, self._source[start:self._pos], "".join(chars), line, col)

    def _escape(self, string_line: int, string_col: int) -> str:
        line, col = self._line, self._col
        self._advance()
        if self._at_end() or self._peek() == "\n":
            raise self._error("unterminated string", string_line, string_col)
        char = self._advance()
        if char not in ESCAPES:
            raise self._error(f"invalid escape sequence '\\{char}'", line, col)
        return ESCAPES[char]

    def _number(self, line: int, col: int, start: int) -> Token:
        self._advance()
        while is_digit(self._peek()):
            self._advance()
        text = self._source[start:self._pos]
        return Token(TokenType.NUMBER, text, int(text), line, col)

    def _word(self, line: int, col: int, start: int) -> Token:
        while is_ident_part(self._peek()):
            self._advance()
        text = self._source[start:self._pos]
        token_type = KEYWORDS.get(text, TokenType.IDENT)
        return Token(token_type, text, text, line, col)

    def _symbol(self, line: int, col: int) -> Token:
        if self._peek() == "=" and self._peek(1) == "=":
            self._advance()
            self._advance()
            return Token(TokenType.EQUALS, "==", "==", line, col)
        char = self._peek()
        token_type = SYMBOLS.get(char)
        if token_type is None:
            raise self._error(f"unexpected character {char!r}", line, col)
        self._advance()
        return Token(token_type, char, char, line, col)

    def _skip_whitespace_and_comments(self) -> None:
        while not self._at_end():
            char = self._peek()
            if char in WHITESPACE:
                self._advance()
            elif char == "#":
                while not self._at_end() and self._peek() != "\n":
                    self._advance()
            else:
                return

    def _at_end(self) -> bool:
        return self._pos >= len(self._source)

    def _peek(self, offset: int = 0) -> str:
        index = self._pos + offset
        return self._source[index] if index < len(self._source) else ""

    def _advance(self) -> str:
        char = self._source[self._pos]
        self._pos += 1
        if char == "\n":
            self._line += 1
            self._col = 1
        else:
            self._col += 1
        return char

    @staticmethod
    def _error(message: str, line: int, col: int) -> CompileError:
        return CompileError(ErrorKind.LEXICAL, message, line, col)


def tokenize(source: str) -> list[Token]:
    return Lexer(source).tokenize()
