from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    TEST = "'TEST'"
    BASE = "'BASE'"
    GET = "'GET'"
    POST = "'POST'"
    PUT = "'PUT'"
    DELETE = "'DELETE'"
    EXPECT = "'EXPECT'"
    STATUS = "'STATUS'"
    JSON = "'JSON'"
    SAVE = "'SAVE'"
    BODY = "'BODY'"
    HEADER = "'HEADER'"
    TRUE = "'true'"
    FALSE = "'false'"
    NULL = "'null'"
    IDENT = "identifier"
    STRING = "string"
    NUMBER = "number"
    LBRACE = "'{'"
    RBRACE = "'}'"
    SEMICOLON = "';'"
    COLON = "':'"
    COMMA = "','"
    PLUS = "'+'"
    ASSIGN = "'='"
    EQUALS = "'=='"
    EOF = "end of file"


KEYWORDS: dict[str, TokenType] = {
    "TEST": TokenType.TEST,
    "BASE": TokenType.BASE,
    "GET": TokenType.GET,
    "POST": TokenType.POST,
    "PUT": TokenType.PUT,
    "DELETE": TokenType.DELETE,
    "EXPECT": TokenType.EXPECT,
    "STATUS": TokenType.STATUS,
    "JSON": TokenType.JSON,
    "SAVE": TokenType.SAVE,
    "BODY": TokenType.BODY,
    "HEADER": TokenType.HEADER,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "null": TokenType.NULL,
}

SYMBOLS: dict[str, TokenType] = {
    "{": TokenType.LBRACE,
    "}": TokenType.RBRACE,
    ";": TokenType.SEMICOLON,
    ":": TokenType.COLON,
    ",": TokenType.COMMA,
    "+": TokenType.PLUS,
    "=": TokenType.ASSIGN,
}


@dataclass(frozen=True)
class Token:
    type: TokenType
    text: str
    value: str | int | None
    line: int
    col: int
