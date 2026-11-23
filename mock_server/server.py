import json
import socket
import threading
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

TOKEN = "secret-token-123"
CREDENTIALS = {"admin": "123"}
MAX_BODY = 64 * 1024
DRAIN_LIMIT = 1024 * 1024


class HttpError(Exception):
    def __init__(self, status: HTTPStatus, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.message = message


class UserStore:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._users = {
            1: {"id": 1, "name": "Alice", "tags": ["admin", "dev"]},
            2: {"id": 2, "name": "Bob", "tags": ["dev"]},
        }
        self._next_id = 3

    def all(self) -> list[dict]:
        with self._lock:
            return [dict(self._users[key]) for key in sorted(self._users)]

    def get(self, user_id: int) -> dict | None:
        with self._lock:
            user = self._users.get(user_id)
            return dict(user) if user is not None else None

    def create(self, name: str) -> dict:
        with self._lock:
            user = {"id": self._next_id, "name": name, "tags": []}
            self._users[self._next_id] = user
            self._next_id += 1
            return dict(user)

    def rename(self, user_id: int, name: str) -> dict | None:
        with self._lock:
            user = self._users.get(user_id)
            if user is None:
                return None
            user["name"] = name
            return dict(user)

    def delete(self, user_id: int) -> bool:
        with self._lock:
            return self._users.pop(user_id, None) is not None


class MockServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address: tuple[str, int], quiet: bool, store: UserStore) -> None:
        super().__init__(address, Handler)
        self.store = store
        self.quiet = quiet


class MockServerIPv6(MockServer):
    address_family = socket.AF_INET6


def require_method(method: str, *allowed: str) -> None:
    if method not in allowed:
        raise HttpError(HTTPStatus.METHOD_NOT_ALLOWED, f"method {method} not allowed")


def parse_user_id(raw: str) -> int:
    if not raw.isdigit():
        raise HttpError(HTTPStatus.NOT_FOUND, "user not found")
    return int(raw)


def required_name(data: dict) -> str:
    name = data.get("name")
    if not isinstance(name, str) or not name:
        raise HttpError(HTTPStatus.BAD_REQUEST, 'field "name" must be a non-empty string')
    return name


def found(user: dict | None) -> dict:
    if user is None:
        raise HttpError(HTTPStatus.NOT_FOUND, "user not found")
    return user


class Handler(BaseHTTPRequestHandler):
    server: MockServer

    def do_GET(self) -> None:
        self._dispatch("GET")

    def do_POST(self) -> None:
        self._dispatch("POST")

    def do_PUT(self) -> None:
        self._dispatch("PUT")

    def do_DELETE(self) -> None:
        self._dispatch("DELETE")

    def log_message(self, format: str, *args) -> None:
        if not self.server.quiet:
            super().log_message(format, *args)

    def _dispatch(self, method: str) -> None:
        segments = urlsplit(self.path).path.strip("/").split("/")
        try:
            status, body = self._route(method, segments)
        except HttpError as error:
            status, body = error.status, {"error": error.message}
        self._respond(status, body)

    def _route(self, method: str, segments: list[str]) -> tuple[HTTPStatus, dict | None]:
        store = self.server.store
        match segments:
            case ["login"]:
                require_method(method, "POST")
                return self._login()
            case ["me"]:
                require_method(method, "GET")
                return self._me()
            case ["users"]:
                require_method(method, "GET", "POST")
                if method == "GET":
                    users = store.all()
                    return HTTPStatus.OK, {"items": users, "count": len(users)}
                return HTTPStatus.CREATED, store.create(required_name(self._json_body()))
            case ["users", raw_id]:
                require_method(method, "GET", "PUT", "DELETE")
                user_id = parse_user_id(raw_id)
                if method == "GET":
                    return HTTPStatus.OK, found(store.get(user_id))
                if method == "PUT":
                    return HTTPStatus.OK, found(store.rename(user_id, required_name(self._json_body())))
                if not store.delete(user_id):
                    raise HttpError(HTTPStatus.NOT_FOUND, "user not found")
                return HTTPStatus.NO_CONTENT, None
        raise HttpError(HTTPStatus.NOT_FOUND, "not found")

    def _login(self) -> tuple[HTTPStatus, dict]:
        data = self._json_body()
        user, password = data.get("user"), data.get("pass")
        if not isinstance(user, str) or CREDENTIALS.get(user) != password:
            raise HttpError(HTTPStatus.UNAUTHORIZED, "invalid credentials")
        return HTTPStatus.OK, {"token": TOKEN, "user": user}

    def _me(self) -> tuple[HTTPStatus, dict]:
        if self.headers.get("Authorization") != f"Bearer {TOKEN}":
            raise HttpError(HTTPStatus.UNAUTHORIZED, "unauthorized")
        return HTTPStatus.OK, {"user": "admin", "role": "admin"}

    def _json_body(self) -> dict:
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            raise HttpError(HTTPStatus.BAD_REQUEST, "invalid Content-Length") from None
        if length < 0:
            raise HttpError(HTTPStatus.BAD_REQUEST, "invalid Content-Length")
        if length > MAX_BODY:
            self._drain(length)
            raise HttpError(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, "request body too large")
        try:
            data = json.loads(self.rfile.read(length))
        except (ValueError, UnicodeDecodeError):
            raise HttpError(HTTPStatus.BAD_REQUEST, "invalid JSON body") from None
        if not isinstance(data, dict):
            raise HttpError(HTTPStatus.BAD_REQUEST, "JSON body must be an object")
        return data

    def _drain(self, length: int) -> None:
        self.close_connection = True
        remaining = min(length, DRAIN_LIMIT)
        while remaining > 0:
            chunk = self.rfile.read(min(remaining, 64 * 1024))
            if not chunk:
                return
            remaining -= len(chunk)

    def _respond(self, status: HTTPStatus, body: dict | None) -> None:
        payload = b"" if body is None else json.dumps(body).encode("utf-8")
        self.send_response(status)
        if body is not None:
            self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def create_server(
    host: str = "127.0.0.1", port: int = 8000, quiet: bool = False, store: UserStore | None = None
) -> MockServer:
    server_class = MockServerIPv6 if ":" in host else MockServer
    return server_class((host, port), quiet, store if store is not None else UserStore())


def create_localhost_servers(port: int = 8000, quiet: bool = False) -> list[MockServer]:
    ipv4 = create_server("127.0.0.1", port, quiet)
    if not socket.has_ipv6:
        return [ipv4]
    try:
        ipv6 = create_server("::1", ipv4.server_address[1], quiet, ipv4.store)
    except OSError:
        return [ipv4]
    return [ipv4, ipv6]
