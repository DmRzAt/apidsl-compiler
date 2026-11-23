import sys
import types

import pytest
import requests

from apidsl.codegen import function_names, generate
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


class FakeResponse:
    def __init__(self, status_code=200, body=None):
        self.status_code = status_code
        self._body = body

    def json(self):
        return self._body


class FakeHttp:
    def __init__(self, *responses):
        self.responses = list(responses)
        self.calls = []

    def request(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        return self.responses.pop(0) if self.responses else FakeResponse()


@pytest.fixture
def http(monkeypatch):
    fake = FakeHttp()
    module = types.ModuleType("requests")
    module.request = fake.request
    module.RequestException = requests.RequestException
    monkeypatch.setitem(sys.modules, "requests", module)
    return fake


def load(source: str, name: str = "example.api") -> dict:
    namespace = {"__name__": "generated"}
    exec(compile(generate(parse(source), name), "generated.py", "exec"), namespace)
    return namespace


def generated_tests(namespace: dict) -> list[str]:
    return [name for name in namespace if name.startswith("test_")]


def failure(call) -> str:
    with pytest.raises(AssertionError) as caught:
        call()
    return str(caught.value)


def dsl_string(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")
    return f'"{escaped}"'


def test_example_sends_the_expected_requests(http):
    http.responses = [FakeResponse(200, {"token": "abc"}), FakeResponse(200, {"role": "admin"})]
    namespace = load(EXAMPLE)

    namespace["test_login_flow"]()

    assert http.calls == [
        (
            "POST",
            "http://localhost:8000/login",
            {"headers": None, "json": {"user": "admin", "pass": "123"}, "timeout": 10},
        ),
        (
            "GET",
            "http://localhost:8000/me",
            {"headers": {"Authorization": "Bearer abc"}, "json": None, "timeout": 10},
        ),
    ]


def test_one_function_per_test(http):
    namespace = load('TEST "A" { GET "http://h/"; } TEST "B" { GET "http://h/"; }')

    assert generated_tests(namespace) == ["test_a", "test_b"]


def test_status_failure_names_the_dsl_line(http):
    http.responses = [FakeResponse(401, {})]
    namespace = load(EXAMPLE)

    assert failure(namespace["test_login_flow"]) == "line 5: expected status 200, got 401"


def test_json_failure_names_the_dsl_line(http):
    http.responses = [FakeResponse(200, {"token": "t"}), FakeResponse(200, {"role": "guest"})]
    namespace = load(EXAMPLE)

    assert failure(namespace["test_login_flow"]) == (
        'line 10: expected JSON "role" == "admin", got "guest"'
    )


def test_saved_number_is_rendered_as_text_in_urls(http):
    http.responses = [FakeResponse(201, {"id": 7})]
    namespace = load(
        'BASE "http://h";\n'
        'TEST "t" { POST "/users" BODY { }; SAVE id = JSON "id"; GET "/users/" + id + "/posts"; }'
    )

    namespace["test_t"]()

    assert http.calls[1][1] == "http://h/users/7/posts"


def test_body_keeps_json_types_of_literals_and_variables(http):
    http.responses = [FakeResponse(200, {"id": 7})]
    namespace = load(
        'BASE "http://h";\n'
        'TEST "t" { GET "/"; SAVE id = JSON "id";\n'
        'POST "/x" BODY { "ref": id, "n": -3, "ok": true, "no": false, "z": null, '
        '"o": { "s": "t" } }; }'
    )

    namespace["test_t"]()

    assert http.calls[1][2]["json"] == {
        "ref": 7, "n": -3, "ok": True, "no": False, "z": None, "o": {"s": "t"}
    }


def test_variable_names_cannot_clash_with_python(http):
    http.responses = [FakeResponse(200, {"a": 1, "b": "x"})]
    namespace = load(
        'BASE "http://h";\n'
        'TEST "t" { GET "/"; SAVE class = JSON "a"; SAVE response = JSON "b"; '
        'GET "/" + class + response; EXPECT STATUS 200; }'
    )

    namespace["test_t"]()

    assert http.calls[1][1] == "http://h/1x"


def test_absolute_url_without_base(http):
    namespace = load('TEST "t" { DELETE "https://api.example.com/x"; }')

    namespace["test_t"]()

    assert namespace["BASE"] is None
    assert http.calls[0][:2] == ("DELETE", "https://api.example.com/x")


def test_hostile_strings_stay_data(http):
    hostile = 'a\'b"c\\d\ne\t{f}"""\'\'\'; __import__("os") #'
    http.responses = [FakeResponse(200, {hostile: hostile})]
    source = (
        f'BASE {dsl_string("http://h")};\n'
        f'TEST {dsl_string(hostile)} {{\n'
        f'  PUT {dsl_string("/" + hostile)} BODY {{ {dsl_string(hostile)}: {dsl_string(hostile)} }} '
        f'HEADER {dsl_string("X-Test")} = {dsl_string(hostile)};\n'
        f'  EXPECT JSON {dsl_string(hostile)} == {dsl_string(hostile)};\n'
        "}"
    )
    namespace = load(source)
    (test_name,) = generated_tests(namespace)

    namespace[test_name]()

    method, url, kwargs = http.calls[0]
    assert url == "http://h/" + hostile
    assert kwargs["json"] == {hostile: hostile}
    assert kwargs["headers"] == {"X-Test": hostile}
    assert test_name.isidentifier()


def test_source_name_cannot_break_out_of_the_header_comment():
    code = generate(parse('TEST "t" { GET "http://h/"; }'), "dir/evil\nimport os.api")

    assert code.splitlines()[0] == "# Generated by apidsl from 'evil\\nimport os.api'. Do not edit."


@pytest.mark.parametrize(
    "names, expected",
    [
        (["Login flow"], ["test_login_flow"]),
        (["Logowanie użytkownika"], ["test_logowanie_uzytkownika"]),
        (["  Get  user #1!  "], ["test_get_user_1"]),
        (["123"], ["test_123"]),
        (["!!!", ""], ["test_unnamed", "test_unnamed_2"]),
        (["A b", "a-b", "a_b"], ["test_a_b", "test_a_b_2", "test_a_b_3"]),
    ],
)
def test_function_names(names, expected):
    assert function_names(names) == expected


def test_generated_tests_are_independent(http):
    http.responses = [FakeResponse(500), FakeResponse(200)]
    namespace = load(
        'BASE "http://h";\n'
        'TEST "a" { GET "/a"; EXPECT STATUS 200; }\n'
        'TEST "b" { GET "/b"; EXPECT STATUS 200; }'
    )

    assert failure(namespace["test_a"]) == "line 2: expected status 200, got 500"
    namespace["test_b"]()
