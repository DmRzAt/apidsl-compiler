import pytest

from apidsl.errors import ErrorKind
from apidsl.parser import parse
from apidsl.semantic import analyze

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


def errors(source: str) -> list[tuple[int, int, str]]:
    return [(e.line, e.col, e.message) for e in analyze(parse(source))]


def in_test(*lines: str) -> str:
    return 'BASE "http://h";\nTEST "t" {\n' + "\n".join(lines) + "\n}"


def test_example_program_is_valid():
    assert errors(EXAMPLE) == []


def test_variable_used_before_save_in_url():
    assert errors(in_test('GET "/u/" + id;')) == [(3, 13, "variable 'id' is used before SAVE")]


def test_variable_used_before_save_in_header():
    assert errors(in_test('GET "/" HEADER "A" = tok;')) == [
        (3, 22, "variable 'tok' is used before SAVE")
    ]


def test_variable_used_before_save_in_nested_body():
    assert errors(in_test('POST "/" BODY { "a": { "b": v } };')) == [
        (3, 29, "variable 'v' is used before SAVE")
    ]


def test_variable_used_before_save_in_expected_value():
    assert errors(in_test('GET "/";', 'EXPECT JSON "k" == x;')) == [
        (4, 20, "variable 'x' is used before SAVE")
    ]


def test_variable_saved_before_use_is_valid():
    source = in_test(
        'GET "/";',
        'SAVE x = JSON "a";',
        'POST "/" + x BODY { "v": x } HEADER "H" = x;',
        'EXPECT JSON "b" == x;',
    )

    assert errors(source) == []


def test_save_after_use_does_not_help():
    assert errors(in_test('GET "/" + x;', 'SAVE x = JSON "a";')) == [
        (3, 11, "variable 'x' is used before SAVE")
    ]


def test_variables_are_scoped_to_their_test():
    source = (
        'BASE "http://h";\n'
        'TEST "a" {\nGET "/";\nSAVE x = JSON "k";\n}\n'
        'TEST "b" {\nGET "/" + x;\n}'
    )

    assert errors(source) == [(7, 11, "variable 'x' is used before SAVE")]


def test_every_undefined_use_is_reported():
    assert errors(in_test('GET "/" + x + x;')) == [
        (3, 11, "variable 'x' is used before SAVE"),
        (3, 15, "variable 'x' is used before SAVE"),
    ]


@pytest.mark.parametrize(
    "statement, label",
    [
        ("EXPECT STATUS 200;", "EXPECT STATUS"),
        ('EXPECT JSON "a" == 1;', "EXPECT JSON"),
        ('SAVE x = JSON "a";', "SAVE"),
    ],
)
def test_response_statement_before_any_request(statement, label):
    assert errors(in_test(statement, 'GET "/";')) == [
        (3, 1, f"{label} before any request in test 't'")
    ]


def test_save_before_request_still_defines_the_variable():
    assert errors(in_test('SAVE x = JSON "k";', 'GET "/" + x;')) == [
        (3, 1, "SAVE before any request in test 't'")
    ]


def test_response_statements_after_request_are_valid():
    source = in_test('GET "/";', "EXPECT STATUS 200;", 'EXPECT JSON "a" == 1;', 'SAVE x = JSON "a";')

    assert errors(source) == []


def test_duplicate_test_names_report_every_repeat():
    source = (
        'TEST "same" { GET "http://h/"; }\n'
        'TEST "other" { GET "http://h/"; }\n'
        'TEST "same" { GET "http://h/"; }\n'
        'TEST "same" { GET "http://h/"; }'
    )

    assert errors(source) == [
        (3, 1, "duplicate test name 'same' (first defined at line 1)"),
        (4, 1, "duplicate test name 'same' (first defined at line 1)"),
    ]


def test_test_names_are_case_sensitive():
    assert errors('TEST "Same" { GET "http://h/"; }\nTEST "same" { GET "http://h/"; }') == []


@pytest.mark.parametrize("code", [-1, 0, 99, 600, 999])
def test_status_outside_range(code):
    assert errors(in_test('GET "/";', f"EXPECT STATUS {code};")) == [
        (4, 1, f"status code {code} is outside 100-599")
    ]


@pytest.mark.parametrize("code", [100, 200, 404, 599])
def test_status_inside_range(code):
    assert errors(in_test('GET "/";', f"EXPECT STATUS {code};")) == []


def test_relative_path_without_base():
    assert errors('TEST "t" {\nGET "/users";\n}') == [
        (2, 5, "relative path '/users' requires BASE")
    ]


def test_every_relative_request_without_base_is_reported():
    assert errors('TEST "t" {\nGET "/a";\nDELETE "/b";\n}') == [
        (2, 5, "relative path '/a' requires BASE"),
        (3, 8, "relative path '/b' requires BASE"),
    ]


@pytest.mark.parametrize(
    "source",
    [
        'BASE "http://h";\nTEST "t" { GET "/users"; }',
        'TEST "t" { GET "http://h/users"; }',
        'TEST "t" { GET "http://h" + "/users"; }',
    ],
)
def test_paths_that_do_not_need_base(source):
    assert errors(source) == []


def test_url_starting_with_variable_is_not_checked_for_base():
    messages = [message for _, _, message in errors('TEST "t" { GET host + "/x"; }')]

    assert messages == ["variable 'host' is used before SAVE"]


def test_empty_test():
    assert errors('BASE "http://h";\nTEST "empty" { }') == [(2, 1, "test 'empty' is empty")]


def test_all_errors_are_collected_in_source_order():
    source = 'TEST "dup" {\nEXPECT STATUS 700;\nGET "/x" + v;\n}\nTEST "dup" { }'

    assert errors(source) == [
        (2, 1, "EXPECT STATUS before any request in test 'dup'"),
        (2, 1, "status code 700 is outside 100-599"),
        (3, 5, "relative path '/x' requires BASE"),
        (3, 12, "variable 'v' is used before SAVE"),
        (5, 1, "duplicate test name 'dup' (first defined at line 1)"),
        (5, 1, "test 'dup' is empty"),
    ]


def test_errors_are_semantic_kind():
    found = analyze(parse('TEST "t" { }\nTEST "t" { EXPECT STATUS 1; }'))

    assert found
    assert {error.kind for error in found} == {ErrorKind.SEMANTIC}
