import os
from typing import Dict
import pyautogui
import random
import string
from datetime import datetime
import socket
import subprocess


def get_local_ip() -> str:
    """Get the local IP address of the machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(("10.254.254.254", 1))  # Use an unreachable IP address
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"  # Fallback to localhost
    finally:
        s.close()
    return ip


def generate_image_name() -> str:
    """Generate a random image name with a timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_str = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"screenshot_{timestamp}_{random_str}.png"


def take_screenshot() -> Dict[str, str]:
    """Take a screenshot of the desktop and save it in a folder."""
    try:
        # Ensure the screenshot directory exists
        screenshot_folder = "_config/data/screenshot"
        os.makedirs(screenshot_folder, exist_ok=True)
        ip = get_local_ip()
        # Generate a unique image name
        image_name = generate_image_name()

        # Capture the screenshot
        screenshot_path = os.path.join(screenshot_folder, image_name)
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)

        # Generate the URL for the screenshot, based on the IP and port
        screenshot_url = f"http://{ip}:8766/_config/data/screenshot/{image_name}"

        return {"status": "success", "url": screenshot_url}

    except Exception as e:
        return {"status": "error", "message": str(e)}


# Define the actions that can be executed when a valid secret_code is provided
def shutdown_pc() -> dict:
    """Shutdown the PC."""
    try:
        # Attempt a safe shutdown
        subprocess.run(["shutdown", "/s", "/t", "0"], check=True)
        return {"status": "success", "message": "PC is shutting down safely."}
    except subprocess.CalledProcessError as _:
        print("Safe shutdown failed, attempting forced shutdown.")
        try:
            # Fall back to forced shutdown
            subprocess.run(["shutdown", "/s", "/f", "/t", "0"], check=True)
            return {"status": "success", "message": "PC is shutting down forcibly."}
        except subprocess.CalledProcessError as force_error:
            return {
                "status": "error",
                "message": f"Forced shutdown also failed: {force_error}",
            }


def execute_mouse_macro() -> dict:
    """Execute a mouse macro."""
    try:
        # For demonstration, we'll simulate a simple mouse action (click)
        # pyautogui.click(x=100, y=100)  # Click at coordinates (100, 100)
        return {"status": "success", "message": "Mouse macro executed"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def shift_n() -> dict:
    """Simulate pressing Shift + N."""
    try:
        pyautogui.keyDown("shift")
        pyautogui.press("n")
        pyautogui.keyUp("shift")
        return {"status": "success", "message": "Executed Shift + N"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def handle_action(action: str) -> dict:
    """Handle the action based on the requested action string."""
    if action == "shutdown":
        return shutdown_pc()
    elif action == "screenshot":
        return take_screenshot()
    elif action == "mouse_macro":
        return execute_mouse_macro()
    elif action == "skip_yt":
        return shift_n()
    else:
        return {"status": "error", "message": "Unknown action"}
