from dataclasses import dataclass
from enum import StrEnum


class ErrorKind(StrEnum):
    LEXICAL = "LexicalError"
    SYNTAX = "SyntaxError"
    SEMANTIC = "SemanticError"


@dataclass
class CompileError(Exception):
    kind: ErrorKind
    message: str
    line: int
    col: int

    def __str__(self) -> str:
        return f"{self.line}:{self.col}: {self.kind}: {self.message}"

    def format(self, filename: str) -> str:
        return f"{filename}:{self}"
