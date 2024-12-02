import http.server
import socketserver
import threading
import os


def start_http_server(port: int) -> None:
    """Start a simple HTTP server to serve screenshots."""
    handler = http.server.SimpleHTTPRequestHandler
    os.makedirs("_config/data", exist_ok=True)
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving fs server at http://localhost:{port}/")
        httpd.serve_forever()


# Start HTTP server in a separate thread
def start_http_server_in_thread():
    http_server_thread = threading.Thread(
        target=start_http_server, args=(8766,), daemon=True
    )
    http_server_thread.start()
