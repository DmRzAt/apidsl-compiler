import json

import requests

TIMEOUT = 10


def show(value) -> str:
    return json.dumps(value, ensure_ascii=False)


def text(value) -> str:
    return value if isinstance(value, str) else show(value)


def resolve_url(base: str | None, address: str) -> str:
    if base is not None and address.startswith("/"):
        return base.rstrip("/") + address
    return address


def send(method: str, address: str, line: int, headers: dict | None = None, body: dict | None = None):
    try:
        return requests.request(method, address, headers=headers, json=body, timeout=TIMEOUT)
    except requests.RequestException as error:
        raise AssertionError(f"line {line}: {method} {address} failed: {error}") from None


def json_path(response, path: str, line: int):
    try:
        current = response.json()
    except ValueError:
        raise AssertionError(f"line {line}: response body is not valid JSON") from None
    where = f"line {line}: JSON path {show(path)}"
    for key in path.split("."):
        if isinstance(current, dict):
            if key not in current:
                raise AssertionError(f"{where}: key {show(key)} not found")
            current = current[key]
        elif isinstance(current, list):
            if not key.isdigit():
                raise AssertionError(f"{where}: expected a list index, got {show(key)}")
            if int(key) >= len(current):
                raise AssertionError(
                    f"{where}: index {key} out of range for list of length {len(current)}"
                )
            current = current[int(key)]
        else:
            raise AssertionError(f"{where}: cannot read {show(key)} from {type(current).__name__}")
    return current


def same_json(actual, expected) -> bool:
    if isinstance(actual, bool) or isinstance(expected, bool):
        return type(actual) is type(expected) and actual == expected
    if isinstance(actual, dict) and isinstance(expected, dict):
        return actual.keys() == expected.keys() and all(
            same_json(actual[key], expected[key]) for key in actual
        )
    if isinstance(actual, list) and isinstance(expected, list):
        return len(actual) == len(expected) and all(map(same_json, actual, expected))
    if isinstance(actual, (dict, list)) or isinstance(expected, (dict, list)):
        return False
    return actual == expected


def expect_status(response, expected: int, line: int) -> None:
    if response.status_code != expected:
        raise AssertionError(
            f"line {line}: expected status {expected}, got {response.status_code}"
        )


def expect_json(response, path: str, expected, line: int) -> None:
    actual = json_path(response, path, line)
    if not same_json(actual, expected):
        raise AssertionError(
            f"line {line}: expected JSON {show(path)} == {show(expected)}, got {show(actual)}"
        )
