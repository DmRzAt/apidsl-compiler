from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class Method(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


@dataclass(frozen=True)
class Node:
    line: int = field(default=0, compare=False, repr=False, kw_only=True)
    col: int = field(default=0, compare=False, repr=False, kw_only=True)


@dataclass(frozen=True)
class StringLiteral(Node):
    value: str


@dataclass(frozen=True)
class NumberLiteral(Node):
    value: int


@dataclass(frozen=True)
class BoolLiteral(Node):
    value: bool


@dataclass(frozen=True)
class NullLiteral(Node):
    pass


@dataclass(frozen=True)
class VarRef(Node):
    name: str


@dataclass(frozen=True)
class Pair(Node):
    key: str
    value: Value


@dataclass(frozen=True)
class ObjectLiteral(Node):
    pairs: tuple[Pair, ...]


Value = StringLiteral | NumberLiteral | BoolLiteral | NullLiteral | VarRef | ObjectLiteral
Term = StringLiteral | VarRef


@dataclass(frozen=True)
class Expr(Node):
    parts: tuple[Term, ...]


@dataclass(frozen=True)
class Header(Node):
    name: str
    value: Expr


@dataclass(frozen=True)
class Request(Node):
    method: Method
    url: Expr
    body: ObjectLiteral | None
    headers: tuple[Header, ...]


@dataclass(frozen=True)
class ExpectStatus(Node):
    code: int


@dataclass(frozen=True)
class ExpectJson(Node):
    path: str
    expected: Value


@dataclass(frozen=True)
class Save(Node):
    name: str
    path: str


Statement = Request | ExpectStatus | ExpectJson | Save


@dataclass(frozen=True)
class Test(Node):
    name: str
    statements: tuple[Statement, ...]


@dataclass(frozen=True)
class Base(Node):
    url: str


@dataclass(frozen=True)
class Program(Node):
    base: Base | None
    tests: tuple[Test, ...]
