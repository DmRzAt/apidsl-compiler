import socket
import threading

import pytest
import requests

from mock_server.server import MAX_BODY, TOKEN, create_localhost_servers

AUTH = {"Authorization": f"Bearer {TOKEN}"}


def call(method: str, url: str, **kwargs) -> requests.Response:
    return requests.request(method, url, timeout=5, **kwargs)


def test_login_returns_token(mock_api):
    response = call("POST", f"{mock_api}/login", json={"user": "admin", "pass": "123"})

    assert response.status_code == 200
    assert response.json() == {"token": TOKEN, "user": "admin"}


def test_login_rejects_wrong_password(mock_api):
    response = call("POST", f"{mock_api}/login", json={"user": "admin", "pass": "x"})

    assert response.status_code == 401
    assert response.json() == {"error": "invalid credentials"}


def test_invalid_json_body(mock_api):
    response = call("POST", f"{mock_api}/login", data="{oops", headers={"Content-Type": "application/json"})

    assert response.status_code == 400
    assert response.json() == {"error": "invalid JSON body"}


def test_json_body_must_be_an_object(mock_api):
    response = call("POST", f"{mock_api}/login", json=["admin", "123"])

    assert response.status_code == 400


def test_body_too_large(mock_api):
    response = call("POST", f"{mock_api}/users", data=b"x" * (MAX_BODY + 1))

    assert response.status_code == 413


def test_me_requires_token(mock_api):
    assert call("GET", f"{mock_api}/me").status_code == 401
    assert call("GET", f"{mock_api}/me", headers={"Authorization": "Bearer nope"}).status_code == 401


def test_me_with_token(mock_api):
    response = call("GET", f"{mock_api}/me", headers=AUTH)

    assert response.status_code == 200
    assert response.json() == {"user": "admin", "role": "admin"}


def test_list_users(mock_api):
    response = call("GET", f"{mock_api}/users")

    assert response.status_code == 200
    assert [user["id"] for user in response.json()["items"]] == [1, 2]
    assert response.json()["count"] == 2


def test_get_user(mock_api):
    response = call("GET", f"{mock_api}/users/1")

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Alice", "tags": ["admin", "dev"]}


def test_unknown_user(mock_api):
    assert call("GET", f"{mock_api}/users/999").status_code == 404
    assert call("GET", f"{mock_api}/users/abc").status_code == 404


def test_create_then_get_user(mock_api):
    created = call("POST", f"{mock_api}/users", json={"name": "Carol"})

    assert created.status_code == 201
    assert created.json() == {"id": 3, "name": "Carol", "tags": []}
    assert call("GET", f"{mock_api}/users/3").json()["name"] == "Carol"


def test_create_user_requires_name(mock_api):
    assert call("POST", f"{mock_api}/users", json={}).status_code == 400
    assert call("POST", f"{mock_api}/users", json={"name": 5}).status_code == 400


def test_update_user(mock_api):
    response = call("PUT", f"{mock_api}/users/2", json={"name": "Robert"})

    assert response.status_code == 200
    assert call("GET", f"{mock_api}/users/2").json()["name"] == "Robert"


def test_delete_user(mock_api):
    assert call("DELETE", f"{mock_api}/users/2").status_code == 204
    assert call("GET", f"{mock_api}/users/2").status_code == 404
    assert call("DELETE", f"{mock_api}/users/2").status_code == 404


def test_unknown_path_and_wrong_method(mock_api):
    assert call("GET", f"{mock_api}/nope").status_code == 404
    assert call("DELETE", f"{mock_api}/login").status_code == 405


def test_query_string_is_ignored_for_routing(mock_api):
    assert call("GET", f"{mock_api}/users/1?verbose=1").status_code == 200


def test_localhost_serves_ipv4_and_ipv6_loopback_with_one_store():
    if not socket.has_ipv6:
        pytest.skip("IPv6 not available")
    servers = create_localhost_servers(port=0, quiet=True)
    threads = [threading.Thread(target=s.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True) for s in servers]
    for thread in threads:
        thread.start()
    try:
        hosts = sorted(server.server_address[0] for server in servers)
        port = servers[0].server_address[1]
        assert hosts == ["127.0.0.1", "::1"]
        created = call("POST", f"http://127.0.0.1:{port}/users", json={"name": "Dana"}).json()
        assert call("GET", f"http://[::1]:{port}/users/{created['id']}").json()["name"] == "Dana"
    finally:
        for server in servers:
            server.shutdown()
            server.server_close()
