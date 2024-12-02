import asyncio
import websockets
import json
from state_manager import set_connection_state
from config import load_secret_code
from websockets.asyncio.server import ServerConnection
from actions import handle_action

HOST = "0.0.0.0"  # Bind to all available network interfaces
PORT = 8765

websocket_running = False  # Flag to track if the WebSocket server is running


async def handle_connection(websocket: ServerConnection) -> None:
    """Handle incoming WebSocket connection."""
    print("New connection established.")
    try:
        # Get connected IP
        client_ip = websocket.remote_address[0]
        print(f"Client IP: {client_ip}")
        set_connection_state("Connected", device=client_ip)
        while True:
            message = await websocket.recv()
            print(f"Received message: {message}")

            if ":" in message:
                secret_code, action = message.split(":", 1)
            else:
                response = {"status": "error", "message": "Invalid format"}
                await websocket.send(json.dumps(response))
                continue

            stored_secret_code = load_secret_code()
            if secret_code != stored_secret_code:
                response = {"status": "error", "message": "Invalid secret code"}
                await websocket.send(json.dumps(response))
                continue

            # Handle the action
            response = handle_action(action)

            # Send the response to the client
            await websocket.send(json.dumps(response))
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed")
        set_connection_state("Disconnected")


async def start_server() -> None:
    """Start the WebSocket server."""
    global websocket_running
    if websocket_running:
        print("WebSocket server is already running.")
        return

    websocket_running = True
    server = await websockets.serve(handle_connection, HOST, PORT)
    print(f"WebSocket server started at ws://{HOST}:{PORT}")
    await server.wait_closed()
    websocket_running = False  # Reset the flag when the server stops


def start_websocket() -> None:
    """Run the WebSocket server in the main event loop of the thread."""
    asyncio.run(start_server())
