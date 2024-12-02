import os
import customtkinter as ctk
from config import save_secret_code, load_secret_code
from connection import start_websocket
import threading
from state_manager import get_connection_state
from typing import Optional
from pystray import Icon, MenuItem, Menu
from PIL import Image

# Initialize CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


def create_gui() -> None:
    """Create and display the main GUI."""
    # Create the main window
    root: ctk.CTk = ctk.CTk()
    root.title("SpongeBob Desktop Client")
    root.geometry("400x350")

    # Secret Code Section
    secret_code_label: ctk.CTkLabel = ctk.CTkLabel(root, text="Enter Secret Code:")
    secret_code_label.pack(pady=10)

    secret_code_entry: ctk.CTkEntry = ctk.CTkEntry(root, placeholder_text="Secret Code")
    secret_code_entry.pack(pady=10)

    # Load saved secret code
    secret_code_entry.insert(0, load_secret_code() or "")

    save_button: ctk.CTkButton = ctk.CTkButton(
        root,
        text="Save Code",
        command=lambda: save_secret_code(secret_code_entry.get()),
    )
    save_button.pack(pady=10)

    # Connection Status
    connection_status_label: ctk.CTkLabel = ctk.CTkLabel(
        root, text="Status: Checking...", text_color="orange"
    )
    connection_status_label.pack(pady=20)

    # Device Info
    device_info_label: ctk.CTkLabel = ctk.CTkLabel(root, text="No device connected")
    device_info_label.pack(pady=10)

    # Save Status
    status_label: ctk.CTkLabel = ctk.CTkLabel(root, text="")
    status_label.pack(pady=10)

    def update_connection_status() -> None:
        """Update connection status and device info based on connection state."""
        state = get_connection_state()  # Get the current state
        status: str = state["status"]
        device: Optional[str] = state["device"]

        # Set connection status text and color
        status_color: str = "red" if status == "Disconnected" else "green"
        connection_status_label.configure(
            text=f"Status: {status}", text_color=status_color
        )

        # Update device information
        if device:
            device_info_label.configure(text=f"Connected to: {device}")
        else:
            device_info_label.configure(text="No device connected")

        root.after(1000, update_connection_status)  # Refresh every second

    # Start connection status updates
    update_connection_status()

    # Run the WebSocket server in a background thread
    websocket_thread: threading.Thread = threading.Thread(
        target=start_websocket, daemon=True
    )
    websocket_thread.start()

    def on_quit(icon, item):
        """Handle quit action."""
        icon.stop()  # Stop the tray icon
        root.quit()  # Quit the GUI

    def restore_window(icon, item):
        """Minimize the GUI and show the tray icon."""
        root.deiconify()
        icon.visible = True  # Make the tray icon visible

    def create_image():
        """Create a simple icon for the system tray."""
        assets_path = os.path.join(os.path.dirname(__file__), "assets", "tray_icon.png")
        if not os.path.exists(assets_path):
            raise FileNotFoundError(f"Icon image not found at {assets_path}")

        image = Image.open(assets_path)

        # Resize the image
        image = image.resize((32, 32), Image.Resampling.LANCZOS)

        return image

    icon_image = create_image()
    tray_menu = Menu(MenuItem("Restore", restore_window), MenuItem("Quit", on_quit))

    # Create and run the tray icon in a background thread
    tray_icon = Icon("SpongeBob", icon_image, menu=tray_menu)
    tray_thread = threading.Thread(target=tray_icon.run, daemon=True)
    tray_thread.start()

    def on_close():
        """Override the window close to minimize to taskbar tray."""
        root.withdraw()  # Hide the window instead of closing it
        tray_icon.visible = True  # Make the tray icon visible

    # Bind the close event to the on_close method
    root.protocol("WM_DELETE_WINDOW", on_close)
    # Run the GUI
    root.mainloop()
