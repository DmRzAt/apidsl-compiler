from dataclasses import dataclass


@dataclass(frozen=True)
class Token:
    type: str
    text: str
    value: str | int | None
    line: int
    col: int
