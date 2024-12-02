import threading
from gui import create_gui
from connection import start_websocket
from fs_server import start_http_server_in_thread


# Start the WebSocket server and HTTP server in separate threads
def start_servers():
    websocket_thread = threading.Thread(target=start_websocket, daemon=True)
    websocket_thread.start()

    start_http_server_in_thread()  # Start the HTTP server to serve screenshots


# Start the GUI application
if __name__ == "__main__":
    start_servers()  # Start the servers in the background
    create_gui()  # Start the GUI
