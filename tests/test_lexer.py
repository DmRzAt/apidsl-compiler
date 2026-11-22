import pytest

from apidsl.errors import CompileError, ErrorKind
from apidsl.lexer import tokenize
from apidsl.tokens import KEYWORDS, TokenType as T


def types(source: str) -> list[T]:
    return [token.type for token in tokenize(source)]


def single(source: str):
    tokens = tokenize(source)
    assert len(tokens) == 2, tokens
    assert tokens[1].type is T.EOF
    return tokens[0]


def lex_error(source: str) -> CompileError:
    with pytest.raises(CompileError) as caught:
        tokenize(source)
    assert caught.value.kind is ErrorKind.LEXICAL
    return caught.value


def test_empty_source_yields_only_eof():
    tokens = tokenize("")

    assert [t.type for t in tokens] == [T.EOF]
    assert (tokens[0].line, tokens[0].col) == (1, 1)


@pytest.mark.parametrize("word, token_type", KEYWORDS.items())
def test_keyword(word, token_type):
    assert single(word).type is token_type


def test_keywords_cover_the_spec():
    assert set(KEYWORDS) == {
        "TEST", "BASE", "GET", "POST", "PUT", "DELETE", "EXPECT", "STATUS",
        "JSON", "SAVE", "BODY", "HEADER", "true", "false", "null",
    }


@pytest.mark.parametrize("word", ["test", "Test", "TRUE", "Null", "TESTS", "GETx", "_GET"])
def test_keywords_are_case_sensitive_and_whole_word(word):
    token = single(word)

    assert token.type is T.IDENT
    assert token.value == word


@pytest.mark.parametrize("word", ["x", "_", "token", "user_id2", "_private", "A9_b"])
def test_identifier(word):
    token = single(word)

    assert token.type is T.IDENT
    assert token.value == word


def test_identifier_rejects_non_ascii_letters():
    error = lex_error("zażółć")

    assert (error.line, error.col) == (1, 3)


@pytest.mark.parametrize("source, value", [("0", 0), ("200", 200), ("-5", -5), ("007", 7)])
def test_number(source, value):
    token = single(source)

    assert token.type is T.NUMBER
    assert token.value == value
    assert token.text == source


def test_minus_without_digit_is_an_error():
    error = lex_error("- 5")

    assert (error.line, error.col) == (1, 1)
    assert "'-'" in error.message


def test_number_followed_by_letters_splits_by_longest_match():
    assert types("123abc") == [T.NUMBER, T.IDENT, T.EOF]


def test_string_value_excludes_quotes():
    token = single('"/login"')

    assert token.type is T.STRING
    assert token.value == "/login"
    assert token.text == '"/login"'


def test_empty_string():
    assert single('""').value == ""


@pytest.mark.parametrize(
    "source, value",
    [
        (r'"a\"b"', 'a"b'),
        (r'"a\\b"', "a\\b"),
        (r'"a\nb"', "a\nb"),
        (r'"a\tb"', "a\tb"),
        (r'"\\\""', '\\"'),
    ],
)
def test_string_escapes(source, value):
    assert single(source).value == value


def test_hash_inside_string_is_not_a_comment():
    assert single('"#tag"').value == "#tag"


def test_invalid_escape_reports_backslash_position():
    error = lex_error(r'GET "ab\q"')

    assert (error.line, error.col) == (1, 8)
    assert "\\q" in error.message


def test_unterminated_string_reports_opening_quote():
    error = lex_error('GET "/login')

    assert (error.line, error.col) == (1, 5)
    assert "unterminated" in error.message


def test_raw_newline_inside_string_is_unterminated():
    error = lex_error('"abc\n"')

    assert (error.line, error.col) == (1, 1)
    assert "unterminated" in error.message


def test_backslash_at_end_of_input_is_unterminated():
    error = lex_error('"abc\\')

    assert "unterminated" in error.message


@pytest.mark.parametrize(
    "source, token_type",
    [
        ("{", T.LBRACE),
        ("}", T.RBRACE),
        (";", T.SEMICOLON),
        (":", T.COLON),
        (",", T.COMMA),
        ("+", T.PLUS),
        ("=", T.ASSIGN),
        ("==", T.EQUALS),
    ],
)
def test_symbol(source, token_type):
    token = single(source)

    assert token.type is token_type
    assert token.text == source


def test_double_equals_wins_over_single():
    assert types("===") == [T.EQUALS, T.ASSIGN, T.EOF]
    assert types("= =") == [T.ASSIGN, T.ASSIGN, T.EOF]


@pytest.mark.parametrize("char", ["@", "$", "!", "(", "'", "<", "."])
def test_unexpected_character(char):
    error = lex_error(f"GET {char}")

    assert (error.line, error.col) == (1, 5)
    assert repr(char) in error.message


def test_whitespace_and_comments_are_skipped():
    source = "  # header comment\n\tGET # trailing\r\n  ;  # no newline at end"

    assert types(source) == [T.GET, T.SEMICOLON, T.EOF]


def test_positions_are_one_based_line_and_column():
    source = 'BASE "x";\n\n  TEST\n# c\n\t}'
    positions = [(t.type, t.line, t.col) for t in tokenize(source)]

    assert positions == [
        (T.BASE, 1, 1),
        (T.STRING, 1, 6),
        (T.SEMICOLON, 1, 9),
        (T.TEST, 3, 3),
        (T.RBRACE, 5, 2),
        (T.EOF, 5, 3),
    ]


def test_error_position_on_a_later_line():
    error = lex_error('# one\nSAVE x = JSON "a";\n   @')

    assert (error.line, error.col) == (3, 4)


def test_full_example_program():
    source = '''BASE "http://localhost:8000";

TEST "Login flow" {
    POST "/login" BODY { "user": "admin", "pass": "123" };
    EXPECT STATUS 200;
    SAVE token = JSON "token";

    GET "/me" HEADER "Authorization" = "Bearer " + token;
    EXPECT STATUS 200;
    EXPECT JSON "role" == "admin";
}
'''

    assert types(source) == [
        T.BASE, T.STRING, T.SEMICOLON,
        T.TEST, T.STRING, T.LBRACE,
        T.POST, T.STRING, T.BODY, T.LBRACE,
        T.STRING, T.COLON, T.STRING, T.COMMA, T.STRING, T.COLON, T.STRING,
        T.RBRACE, T.SEMICOLON,
        T.EXPECT, T.STATUS, T.NUMBER, T.SEMICOLON,
        T.SAVE, T.IDENT, T.ASSIGN, T.JSON, T.STRING, T.SEMICOLON,
        T.GET, T.STRING, T.HEADER, T.STRING, T.ASSIGN, T.STRING, T.PLUS, T.IDENT, T.SEMICOLON,
        T.EXPECT, T.STATUS, T.NUMBER, T.SEMICOLON,
        T.EXPECT, T.JSON, T.STRING, T.EQUALS, T.STRING, T.SEMICOLON,
        T.RBRACE,
        T.EOF,
    ]


def test_literal_values_in_example():
    tokens = tokenize('EXPECT JSON "role" == true; SAVE id = JSON "items.0.id";')
    values = [t.value for t in tokens if t.type in (T.STRING, T.IDENT)]

    assert values == ["role", "id", "items.0.id"]
