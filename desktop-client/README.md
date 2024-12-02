# SpongeBob Desktop Client

This is the desktop client of the **SpongeBob** project. It handles the connection with the mobile app via WebSocket and provides a GUI for configuration and status updates.

### Features:

- **Secret Code Input**: Allows the user to input and save a secret code for communication.
- **Connection Status**: Displays real-time status of the WebSocket connection to the mobile app.
- **WebSocket Server**: Runs a WebSocket server to handle communication with the mobile app.

### Project Files:

- **`app.py`**: Entry point for the application. Sets up the GUI and runs the WebSocket server.
- **`config.py`**: Handles the saving and loading of the secret code to a JSON file.
- **`connection.py`**: Starts and manages the WebSocket server, handling connections and messaging.
- **`gui.py`**: Contains the logic for the desktop client’s GUI using `customtkinter`.
- **`state_manager.py`**: Manages the connection state and updates the GUI accordingly.
- **`requirements.txt`**: Lists the dependencies for the project.

### Running the Desktop Client:

1. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:

   ```bash
   python app.py
   ```

3. The app will show a window where you can input a secret code, and it will also display the connection status with the mobile app.

---

### Dependencies:

- **`customtkinter`**: Used for creating the GUI.
- **`websockets`**: Used for WebSocket communication.
- **`threading`**: For running the WebSocket server in the background.
