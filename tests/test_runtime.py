import pytest
import requests

from apidsl import runtime


class FakeResponse:
    def __init__(self, status_code=200, body=None, invalid_json=False):
        self.status_code = status_code
        self._body = body
        self._invalid_json = invalid_json

    def json(self):
        if self._invalid_json:
            raise requests.JSONDecodeError("Expecting value", "", 0)
        return self._body


def failure(call) -> str:
    with pytest.raises(AssertionError) as caught:
        call()
    return str(caught.value)


@pytest.mark.parametrize(
    "base, address, expected",
    [
        ("http://h", "/users", "http://h/users"),
        ("http://h/", "/users", "http://h/users"),
        ("http://h", "http://other/x", "http://other/x"),
        (None, "http://other/x", "http://other/x"),
        (None, "/users", "/users"),
    ],
)
def test_resolve_url(base, address, expected):
    assert runtime.resolve_url(base, address) == expected


@pytest.mark.parametrize(
    "value, expected",
    [("abc", "abc"), (5, "5"), (2.5, "2.5"), (True, "true"), (False, "false"), (None, "null"),
     ({"a": 1}, '{"a": 1}'), ([1, "x"], '[1, "x"]')],
)
def test_text_renders_json_values(value, expected):
    assert runtime.text(value) == expected


def test_json_path_reads_nested_keys_and_list_indexes():
    response = FakeResponse(body={"items": [{"id": 1}, {"id": 2, "tags": ["a", "b"]}]})

    assert runtime.json_path(response, "items.1.id", 7) == 2
    assert runtime.json_path(response, "items.1.tags.0", 7) == "a"


def test_json_path_treats_numeric_segment_as_key_in_objects():
    assert runtime.json_path(FakeResponse(body={"200": "ok"}), "200", 1) == "ok"


def test_json_path_missing_key():
    message = failure(lambda: runtime.json_path(FakeResponse(body={"a": {}}), "a.b", 9))

    assert message == 'line 9: JSON path "a.b": key "b" not found'


def test_json_path_index_out_of_range():
    message = failure(lambda: runtime.json_path(FakeResponse(body={"a": [1]}), "a.3", 4))

    assert message == 'line 4: JSON path "a.3": index 3 out of range for list of length 1'


def test_json_path_non_numeric_segment_on_list():
    message = failure(lambda: runtime.json_path(FakeResponse(body=[1]), "x", 4))

    assert message == 'line 4: JSON path "x": expected a list index, got "x"'


def test_json_path_through_a_scalar():
    message = failure(lambda: runtime.json_path(FakeResponse(body={"a": 5}), "a.b", 2))

    assert message == 'line 2: JSON path "a.b": cannot read "b" from int'


def test_json_path_on_non_json_response():
    message = failure(lambda: runtime.json_path(FakeResponse(invalid_json=True), "a", 3))

    assert message == "line 3: response body is not valid JSON"


def test_expect_status_passes_on_match():
    runtime.expect_status(FakeResponse(status_code=201), 201, 5)


def test_expect_status_reports_line_and_actual_status():
    message = failure(lambda: runtime.expect_status(FakeResponse(status_code=404), 200, 8))

    assert message == "line 8: expected status 200, got 404"


def test_expect_json_passes_on_equal_values():
    runtime.expect_json(FakeResponse(body={"o": {"a": [1, None]}}), "o", {"a": [1, None]}, 1)


def test_expect_json_reports_both_values_as_json():
    response = FakeResponse(body={"role": "user"})
    message = failure(lambda: runtime.expect_json(response, "role", "admin", 10))

    assert message == 'line 10: expected JSON "role" == "admin", got "user"'


@pytest.mark.parametrize(
    "actual, expected",
    [(True, 1), (1, True), (False, 0), (0, False), ({"a": True}, {"a": 1}), ([1], {"0": 1})],
)
def test_same_json_does_not_mix_booleans_and_numbers(actual, expected):
    assert not runtime.same_json(actual, expected)


@pytest.mark.parametrize(
    "actual, expected",
    [(1, 1), (1.0, 1), ("a", "a"), (None, None), ({"a": [1, {"b": False}]}, {"a": [1, {"b": False}]})],
)
def test_same_json_equal_values(actual, expected):
    assert runtime.same_json(actual, expected)


def test_send_uses_timeout_and_passes_headers_and_body(monkeypatch):
    calls = []

    def fake_request(method, url, **kwargs):
        calls.append((method, url, kwargs))
        return FakeResponse()

    monkeypatch.setattr(runtime.requests, "request", fake_request)

    runtime.send("POST", "http://h/x", 3, headers={"A": "1"}, body={"k": "v"})

    assert calls == [("POST", "http://h/x", {"headers": {"A": "1"}, "json": {"k": "v"}, "timeout": 10})]


def test_send_turns_connection_errors_into_assertions(monkeypatch):
    def fail(method, url, **kwargs):
        raise requests.ConnectionError("connection refused")

    monkeypatch.setattr(runtime.requests, "request", fail)
    message = failure(lambda: runtime.send("GET", "http://h/x", 6))

    assert message == "line 6: GET http://h/x failed: connection refused"
