from collections.abc import Iterator
from dataclasses import dataclass

from apidsl import ast
from apidsl.errors import CompileError, ErrorKind

MIN_STATUS = 100
MAX_STATUS = 599

RESPONSE_STATEMENT_LABELS = {
    ast.ExpectStatus: "EXPECT STATUS",
    ast.ExpectJson: "EXPECT JSON",
    ast.Save: "SAVE",
}


@dataclass(frozen=True)
class Symbol:
    name: str
    line: int
    col: int


class SymbolTable:
    def __init__(self) -> None:
        self._symbols: dict[str, Symbol] = {}

    def define(self, symbol: Symbol) -> None:
        self._symbols[symbol.name] = symbol

    def lookup(self, name: str) -> Symbol | None:
        return self._symbols.get(name)


def variable_refs(node: ast.Expr | ast.Value | None) -> Iterator[ast.VarRef]:
    match node:
        case ast.VarRef():
            yield node
        case ast.Expr(parts=parts):
            for part in parts:
                yield from variable_refs(part)
        case ast.ObjectLiteral(pairs=pairs):
            for pair in pairs:
                yield from variable_refs(pair.value)


def request_refs(request: ast.Request) -> Iterator[ast.VarRef]:
    yield from variable_refs(request.url)
    yield from variable_refs(request.body)
    for header in request.headers:
        yield from variable_refs(header.value)


class Analyzer:
    def __init__(self, program: ast.Program) -> None:
        self._program = program
        self._errors: list[CompileError] = []

    def run(self) -> list[CompileError]:
        first_by_name: dict[str, ast.Test] = {}
        for test in self._program.tests:
            first = first_by_name.setdefault(test.name, test)
            if first is not test:
                self._report(
                    test, f"duplicate test name '{test.name}' (first defined at line {first.line})"
                )
            self._check_test(test)
        return sorted(self._errors, key=lambda error: (error.line, error.col))

    def _check_test(self, test: ast.Test) -> None:
        if not test.statements:
            self._report(test, f"test '{test.name}' is empty")
        symbols = SymbolTable()
        has_response = False
        for statement in test.statements:
            if isinstance(statement, ast.Request):
                self._check_request(statement, symbols)
                has_response = True
                continue
            if not has_response:
                label = RESPONSE_STATEMENT_LABELS[type(statement)]
                self._report(statement, f"{label} before any request in test '{test.name}'")
            match statement:
                case ast.ExpectStatus(code=code):
                    self._check_status(statement, code)
                case ast.ExpectJson(expected=expected):
                    self._check_refs(variable_refs(expected), symbols)
                case ast.Save(name=name):
                    symbols.define(Symbol(name, statement.line, statement.col))

    def _check_request(self, request: ast.Request, symbols: SymbolTable) -> None:
        first = request.url.parts[0]
        if (
            self._program.base is None
            and isinstance(first, ast.StringLiteral)
            and first.value.startswith("/")
        ):
            self._report(first, f"relative path '{first.value}' requires BASE")
        self._check_refs(request_refs(request), symbols)

    def _check_status(self, statement: ast.ExpectStatus, code: int) -> None:
        if not MIN_STATUS <= code <= MAX_STATUS:
            self._report(statement, f"status code {code} is outside {MIN_STATUS}-{MAX_STATUS}")

    def _check_refs(self, refs: Iterator[ast.VarRef], symbols: SymbolTable) -> None:
        for ref in refs:
            if symbols.lookup(ref.name) is None:
                self._report(ref, f"variable '{ref.name}' is used before SAVE")

    def _report(self, node: ast.Node, message: str) -> None:
        self._errors.append(CompileError(ErrorKind.SEMANTIC, message, node.line, node.col))


def analyze(program: ast.Program) -> list[CompileError]:
    return Analyzer(program).run()
