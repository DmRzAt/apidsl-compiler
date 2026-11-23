import argparse
import threading

from mock_server.server import create_localhost_servers, create_server


def main() -> None:
    parser = argparse.ArgumentParser(prog="python -m mock_server", description="Mock API for apidsl demos")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    if args.host == "localhost":
        servers = create_localhost_servers(args.port)
    else:
        servers = [create_server(args.host, args.port)]
    port = servers[0].server_address[1]
    addresses = ", ".join(server.server_address[0] for server in servers)
    print(f"Mock API listening on http://{args.host}:{port} ({addresses}); Ctrl+C to stop", flush=True)
    main_server, *other_servers = servers
    for server in other_servers:
        threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        main_server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        for server in servers:
            server.server_close()


if __name__ == "__main__":
    main()
