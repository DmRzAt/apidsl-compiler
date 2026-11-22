from antlr4 import CommonTokenStream, InputStream
from antlr4.Token import Token as AntlrToken
from antlr4.error.ErrorListener import ErrorListener

from apidsl.errors import CompileError, ErrorKind
from apidsl.generated.ApiDslLexer import ApiDslLexer
from apidsl.tokens import Token

ESCAPES = {'"': '"', "\\": "\\", "n": "\n", "t": "\t"}


class LexicalErrorListener(ErrorListener):
    def __init__(self, source: str) -> None:
        self._lines = source.split("\n")

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        char = self._lines[line - 1][column]
        raise CompileError(ErrorKind.LEXICAL, f"unexpected character {char!r}", line, column + 1)


def decode_string(token: AntlrToken) -> str:
    body = token.text[1:-1]
    body_col = token.column + 2
    chars = []
    index = 0
    while index < len(body):
        char = body[index]
        if char != "\\":
            chars.append(char)
            index += 1
            continue
        escaped = body[index + 1]
        if escaped not in ESCAPES:
            raise CompileError(
                ErrorKind.LEXICAL,
                f"invalid escape sequence '\\{escaped}'",
                token.line,
                body_col + index,
            )
        chars.append(ESCAPES[escaped])
        index += 2
    return "".join(chars)


def check_token(token: AntlrToken) -> None:
    if token.type == ApiDslLexer.UNTERMINATED_STRING:
        raise CompileError(ErrorKind.LEXICAL, "unterminated string", token.line, token.column + 1)
    if token.type == ApiDslLexer.STRING:
        decode_string(token)


def lex(source: str) -> CommonTokenStream:
    lexer = ApiDslLexer(InputStream(source))
    lexer.removeErrorListeners()
    lexer.addErrorListener(LexicalErrorListener(source))
    stream = CommonTokenStream(lexer)
    stream.fill()
    for token in stream.tokens:
        check_token(token)
    return stream


def token_value(token: AntlrToken) -> str | int | None:
    if token.type == ApiDslLexer.STRING:
        return decode_string(token)
    if token.type == ApiDslLexer.NUMBER:
        return int(token.text)
    if token.type == AntlrToken.EOF:
        return None
    return token.text


def type_name(token_type: int) -> str:
    if token_type == AntlrToken.EOF:
        return "EOF"
    return ApiDslLexer.symbolicNames[token_type]


def tokenize(source: str) -> list[Token]:
    return [
        Token(
            type_name(token.type),
            "" if token.type == AntlrToken.EOF else token.text,
            token_value(token),
            token.line,
            token.column + 1,
        )
        for token in lex(source).tokens
    ]
