import threading

import pytest

from mock_server.server import create_server


@pytest.fixture
def mock_api():
    server = create_server(port=0, quiet=True)
    thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_address[1]}"
    server.shutdown()
    server.server_close()
    thread.join(timeout=5)
