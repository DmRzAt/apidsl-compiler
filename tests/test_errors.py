import pytest

from apidsl.errors import CompileError, ErrorKind


def test_format_includes_file_position_kind_and_message():
    error = CompileError(ErrorKind.SYNTAX, "expected ';'", 5, 12)

    assert error.format("file.api") == "file.api:5:12: SyntaxError: expected ';'"


def test_compile_error_can_be_raised_and_caught():
    with pytest.raises(CompileError) as caught:
        raise CompileError(ErrorKind.LEXICAL, "unterminated string", 1, 3)

    assert caught.value.kind is ErrorKind.LEXICAL
    assert str(caught.value) == "1:3: LexicalError: unterminated string"
