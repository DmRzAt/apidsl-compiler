import pytest

from apidsl.errors import CompileError, ErrorKind
from apidsl.parser import parse_tree

EXAMPLE = '''BASE "http://localhost:8000";

TEST "Login flow" {
    POST "/login" BODY { "user": "admin", "pass": "123" };
    EXPECT STATUS 200;
    SAVE token = JSON "token";

    GET "/me" HEADER "Authorization" = "Bearer " + token;
    EXPECT STATUS 200;
    EXPECT JSON "role" == "admin";
}
'''


def syntax_error(source: str) -> CompileError:
    with pytest.raises(CompileError) as caught:
        parse_tree(source)
    assert caught.value.kind is ErrorKind.SYNTAX
    return caught.value


@pytest.mark.parametrize(
    "source",
    [
        EXAMPLE,
        'TEST "no base" { GET "http://x/a"; }',
        'TEST "a" { }',
        'TEST "a" { GET "/"; } TEST "b" { DELETE "/"; }',
        'TEST "a" { PUT "/u" BODY { }; }',
        'TEST "a" { POST "/u" BODY { "n": { "m": null } }; }',
        'TEST "a" { POST "/u" BODY { "s": "x", "n": -1, "v": id, "t": true, "f": false, "z": null }; }',
        'TEST "a" { GET base + "/u/" + id HEADER "A" = "1" HEADER "B" = tok; }',
        'TEST "a" { GET "/"; EXPECT JSON "items.0.id" == 7; EXPECT JSON "o" == { "k": 1 }; }',
    ],
)
def test_valid_program_parses(source):
    assert parse_tree(source) is not None


def test_missing_semicolon_after_base():
    error = syntax_error('BASE "x"\nTEST "a" { GET "/"; }')

    assert error.message == "expected ';', got 'TEST'"
    assert (error.line, error.col) == (2, 1)


def test_missing_semicolon_after_request():
    error = syntax_error('TEST "a" {\n  GET "/x"\n  EXPECT STATUS 200;\n}')

    assert error.message == "expected one of 'BODY', 'HEADER', ';', got 'EXPECT'"
    assert (error.line, error.col) == (3, 3)


def test_empty_source_needs_a_test():
    error = syntax_error("")

    assert error.message == "expected one of 'TEST', 'BASE', got end of file"
    assert (error.line, error.col) == (1, 1)


def test_base_alone_needs_a_test():
    error = syntax_error('BASE "x";')

    assert error.message == "expected 'TEST', got end of file"
    assert (error.line, error.col) == (1, 10)


def test_base_after_test_is_rejected():
    error = syntax_error('TEST "a" { }\nBASE "x";')

    assert error.message == "expected one of 'TEST', end of file, got 'BASE'"
    assert (error.line, error.col) == (2, 1)


def test_unknown_statement():
    error = syntax_error('TEST "a" { PATCH "/"; }')

    assert error.message == (
        "expected one of 'GET', 'POST', 'PUT', 'DELETE', 'EXPECT', 'SAVE', '}', got 'PATCH'"
    )
    assert (error.line, error.col) == (1, 12)


def test_unclosed_test_block():
    error = syntax_error('TEST "a" { GET "/";')

    assert error.message.startswith("expected one of 'GET'")
    assert error.message.endswith("'}', got end of file")


def test_trailing_comma_in_object():
    error = syntax_error('TEST "a" { POST "/" BODY { "a": 1, }; }')

    assert error.message == "expected string, got '}'"


def test_status_requires_number():
    error = syntax_error('TEST "a" { GET "/"; EXPECT STATUS "200"; }')

    assert error.message == "expected number, got '\"200\"'"
    assert (error.line, error.col) == (1, 35)


def test_header_requires_assign():
    error = syntax_error('TEST "a" { GET "/" HEADER "A" "b"; }')

    assert error.message == "expected '=', got '\"b\"'"


def test_save_requires_json_keyword():
    error = syntax_error('TEST "a" { GET "/"; SAVE x = "token"; }')

    assert error.message == "expected 'JSON', got '\"token\"'"


def test_json_assertion_requires_double_equals():
    error = syntax_error('TEST "a" { GET "/"; EXPECT JSON "a" = 1; }')

    assert error.message == "expected '==', got '='"


def test_test_name_must_be_a_string():
    error = syntax_error("TEST login { }")

    assert error.message == "expected string, got 'login'"
    assert (error.line, error.col) == (1, 6)


def test_lexical_error_is_reported_before_parsing():
    with pytest.raises(CompileError) as caught:
        parse_tree('TEST "a" { GET @; }')

    assert caught.value.kind is ErrorKind.LEXICAL
    assert (caught.value.line, caught.value.col) == (1, 16)
