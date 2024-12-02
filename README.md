# SpongeBob

SpongeBob is a versatile application that bridges your mobile and desktop, enabling seamless control of your PC directly from your phone.

## Features

- **Shut Down PC**: Remotely power off your computer.
- **Take Screenshots**: Capture your PC screen from your mobile device.
- **Run Mouse Macros**: Automate repetitive mouse tasks with ease.
- **Music Control**: Play, pause, and control your music from the desktop via mobile.
- **Mobile as PC Mic**: Use your phone as a microphone for your PC.
- **PC as Mobile Speaker**: Stream PC audio to your mobile device.

## Components

1. **Desktop Client**

   - Built with Python for executing commands received from the mobile app.
   - Listens for commands such as shutdown, screenshot, or macro execution.

2. **Mobile App**
   - A user-friendly interface for sending commands to the desktop client.

## Requirements

### Desktop Client

- Python 3.9 or later
- Required libraries (install via `requirements.txt`):
  - Flask
  - PyAutoGUI
  - Pillow

### Mobile App

- To be developed in future releases.

## Installation

### Desktop Client

1. Clone this repository:

   ```bash
   git clone https://github.com/KeptCodes/SpongeBob.git
   cd SpongeBob/desktop-client
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the desktop client:

   ```bash
   python app.py
   ```

4. Make sure your desktop and mobile are on the same network.

### Mobile App

Details coming soon.

## Contributing

Contributions are welcome! Please fork this repository, create a new branch, and submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
