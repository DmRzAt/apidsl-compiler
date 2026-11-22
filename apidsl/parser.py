from antlr4.Token import Token as AntlrToken
from antlr4.error.ErrorListener import ErrorListener

from apidsl.errors import CompileError, ErrorKind
from apidsl.generated.ApiDslParser import ApiDslParser
from apidsl.lexer import lex

CATEGORY_NAMES = {
    ApiDslParser.IDENT: "identifier",
    ApiDslParser.NUMBER: "number",
    ApiDslParser.STRING: "string",
}


def describe_type(token_type: int) -> str:
    if token_type == AntlrToken.EOF:
        return "end of file"
    if token_type in CATEGORY_NAMES:
        return CATEGORY_NAMES[token_type]
    return ApiDslParser.literalNames[token_type]


def describe_token(token: AntlrToken) -> str:
    if token.type == AntlrToken.EOF:
        return "end of file"
    return f"'{token.text}'"


def describe_expected(token_types: list[int]) -> str:
    names = [describe_type(t) for t in sorted(token_types, key=lambda t: (t == AntlrToken.EOF, t))]
    if len(names) == 1:
        return names[0]
    return "one of " + ", ".join(names)


class SyntaxErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        expected = describe_expected(list(recognizer.getExpectedTokens()))
        message = f"expected {expected}, got {describe_token(offendingSymbol)}"
        raise CompileError(ErrorKind.SYNTAX, message, line, column + 1)


def parse_tree(source: str) -> ApiDslParser.ProgramContext:
    parser = ApiDslParser(lex(source))
    parser.removeErrorListeners()
    parser.addErrorListener(SyntaxErrorListener())
    return parser.program()
