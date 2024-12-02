from typing import Dict, Optional

# Define the connection state type
connection_state: Dict[str, Optional[str]] = {"status": "Disconnected", "device": ""}


def set_connection_state(status: str, device: Optional[str] = None) -> None:
    """Set the connection state."""
    connection_state["status"] = status
    connection_state["device"] = device if device else ""


def get_connection_state() -> Dict[str, Optional[str]]:
    """Get the current connection state."""
    return connection_state
