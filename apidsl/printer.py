from dataclasses import fields
from enum import Enum

from apidsl import ast
from apidsl.tokens import Token

POSITION_FIELDS = {"line", "col"}


def format_tokens(tokens: list[Token]) -> str:
    rows = (f"{f'{token.line}:{token.col}':<8}{token.type:<12}{token.text}" for token in tokens)
    return "\n".join(row.rstrip() for row in rows)


def scalar(value) -> str:
    return value.value if isinstance(value, Enum) else repr(value)


def append_node(node: ast.Node, label: str, depth: int, lines: list[str]) -> None:
    details = []
    children: list[tuple[str, ast.Node]] = []
    for field in fields(node):
        if field.name in POSITION_FIELDS:
            continue
        value = getattr(node, field.name)
        if isinstance(value, ast.Node):
            children.append((field.name, value))
        elif isinstance(value, tuple):
            children.extend((field.name, item) for item in value)
        elif value is not None:
            details.append(f"{field.name}={scalar(value)}")
    head = " ".join([label + type(node).__name__, *details, f"@{node.line}:{node.col}"])
    lines.append("  " * depth + head)
    for name, child in children:
        append_node(child, f"{name}: ", depth + 1, lines)


def format_ast(node: ast.Node) -> str:
    lines: list[str] = []
    append_node(node, "", 0, lines)
    return "\n".join(lines)
