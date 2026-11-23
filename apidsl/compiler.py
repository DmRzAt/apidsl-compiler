from apidsl import ast
from apidsl.codegen import generate
from apidsl.errors import CompileError
from apidsl.parser import parse
from apidsl.semantic import analyze


class CompilationFailed(Exception):
    def __init__(self, errors: list[CompileError]) -> None:
        super().__init__(f"{len(errors)} compile error(s)")
        self.errors = errors


def check(source: str) -> ast.Program:
    try:
        program = parse(source)
    except CompileError as error:
        raise CompilationFailed([error]) from None
    errors = analyze(program)
    if errors:
        raise CompilationFailed(errors)
    return program


def compile_source(source: str, source_name: str) -> str:
    return generate(check(source), source_name)
