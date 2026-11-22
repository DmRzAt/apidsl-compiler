import pytest

from apidsl.ast import (
    Base,
    BoolLiteral,
    ExpectJson,
    ExpectStatus,
    Expr,
    Header,
    Method,
    NullLiteral,
    NumberLiteral,
    ObjectLiteral,
    Pair,
    Program,
    Request,
    Save,
    StringLiteral,
    VarRef,
)
from apidsl import ast as nodes
from apidsl.errors import CompileError, ErrorKind
from apidsl.parser import parse

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


def only_statement(body: str):
    program = parse(f'TEST "t" {{ {body} }}')
    assert len(program.tests) == 1
    assert len(program.tests[0].statements) == 1
    return program.tests[0].statements[0]


def expected_value(source_value: str):
    statement = only_statement(f'EXPECT JSON "k" == {source_value};')
    assert isinstance(statement, ExpectJson)
    return statement.expected


def url(*parts) -> Expr:
    return Expr(tuple(parts))


def test_example_program():
    assert parse(EXAMPLE) == Program(
        base=Base("http://localhost:8000"),
        tests=(
            nodes.Test(
                "Login flow",
                (
                    Request(
                        Method.POST,
                        url(StringLiteral("/login")),
                        ObjectLiteral(
                            (
                                Pair("user", StringLiteral("admin")),
                                Pair("pass", StringLiteral("123")),
                            )
                        ),
                        (),
                    ),
                    ExpectStatus(200),
                    Save("token", "token"),
                    Request(
                        Method.GET,
                        url(StringLiteral("/me")),
                        None,
                        (Header("Authorization", url(StringLiteral("Bearer "), VarRef("token"))),),
                    ),
                    ExpectStatus(200),
                    ExpectJson("role", StringLiteral("admin")),
                ),
            ),
        ),
    )


def test_program_without_base():
    program = parse('TEST "a" { GET "http://x/"; }')

    assert program.base is None


def test_tests_keep_source_order():
    program = parse('TEST "first" { } TEST "second" { } TEST "third" { }')

    assert [t.name for t in program.tests] == ["first", "second", "third"]
    assert all(t.statements == () for t in program.tests)


@pytest.mark.parametrize("method", list(Method))
def test_every_method(method):
    statement = only_statement(f'{method.value} "/x";')

    assert statement == Request(method, url(StringLiteral("/x")), None, ())


def test_url_concatenation_keeps_term_order():
    statement = only_statement('GET base + "/users/" + id + "/posts";')

    assert statement.url == url(
        VarRef("base"), StringLiteral("/users/"), VarRef("id"), StringLiteral("/posts")
    )


def test_headers_keep_source_order():
    statement = only_statement('GET "/" HEADER "A" = "1" HEADER "B" = tok + "x";')

    assert statement.headers == (
        Header("A", url(StringLiteral("1"))),
        Header("B", url(VarRef("tok"), StringLiteral("x"))),
    )


def test_body_and_headers_together():
    statement = only_statement('PUT "/u" BODY { } HEADER "A" = "1";')

    assert statement.body == ObjectLiteral(())
    assert statement.headers == (Header("A", url(StringLiteral("1"))),)


@pytest.mark.parametrize(
    "source, value",
    [
        ('"text"', StringLiteral("text")),
        ("42", NumberLiteral(42)),
        ("-7", NumberLiteral(-7)),
        ("true", BoolLiteral(True)),
        ("false", BoolLiteral(False)),
        ("null", NullLiteral()),
        ("name", VarRef("name")),
        ("{ }", ObjectLiteral(())),
    ],
)
def test_value_kinds(source, value):
    assert expected_value(source) == value


def test_nested_object():
    assert expected_value('{ "a": { "b": x }, "c": 1 }') == ObjectLiteral(
        (
            Pair("a", ObjectLiteral((Pair("b", VarRef("x")),))),
            Pair("c", NumberLiteral(1)),
        )
    )


def test_string_escapes_are_decoded():
    statement = only_statement(r'EXPECT JSON "a\"b" == "line\nnext";')

    assert statement == ExpectJson('a"b', StringLiteral("line\nnext"))


def test_save():
    assert only_statement('SAVE user_id = JSON "items.0.id";') == Save("user_id", "items.0.id")


def test_expect_status_keeps_any_number():
    assert only_statement("EXPECT STATUS 999;") == ExpectStatus(999)


def test_positions_point_at_first_token():
    program = parse('BASE "b";\nTEST "a" {\n  GET "/x" + id;\n  EXPECT STATUS 200;\n}')
    test = program.tests[0]
    request, expect = test.statements

    assert (program.base.line, program.base.col) == (1, 1)
    assert (test.line, test.col) == (2, 1)
    assert (request.line, request.col) == (3, 3)
    assert (request.url.line, request.url.col) == (3, 7)
    assert (request.url.parts[1].line, request.url.parts[1].col) == (3, 14)
    assert (expect.line, expect.col) == (4, 3)


def test_positions_of_values_and_saves():
    program = parse('TEST "a" {\n  SAVE x = JSON "p";\n  EXPECT JSON "k" == { "n": v };\n}')
    save, expect = program.tests[0].statements
    pair = expect.expected.pairs[0]

    assert (save.line, save.col) == (2, 3)
    assert (expect.expected.line, expect.expected.col) == (3, 22)
    assert (pair.line, pair.col) == (3, 24)
    assert (pair.value.line, pair.value.col) == (3, 29)


def test_positions_do_not_affect_equality():
    assert StringLiteral("x", line=1, col=1) == StringLiteral("x", line=9, col=9)


def test_syntax_errors_still_raise():
    with pytest.raises(CompileError) as caught:
        parse('TEST "a" { GET "/" }')

    assert caught.value.kind is ErrorKind.SYNTAX
