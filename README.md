# Captain's Voice Commander

This Python script utilizes Dragonfly for speech recognition on Windows and pydirectinput for direct input into DirectX games, such as Star Citizen, which this project is originally based on and was created for. However, this program should work for any other program/DirectX game if you would like.

Dragonfly: [https://pypi.org/project/dragonfly2/](https://pypi.org/project/dragonfly2/)
PyDirectInput: [https://pypi.org/project/PyDirectInput/](https://pypi.org/project/PyDirectInput/)

## Features

- **Custom Voice Commands:** Define your own voice commands and keybindings for controlling your computer.
- **Wake Word Recognition:** Use a wake word (e.g., "Jarvis") to activate voice commands, similar to virtual assistant programs.
- **Push-to-Talk:** Enable push-to-talk functionality for voice commands, ensuring commands are only recognized when a specific key is pressed.
- **Graphical User Interface:** Interact with the program through a simple GUI built with Tkinter, making it easy to add, edit, and delete commands.
- **Open Webpages as a Voice Command:** This feature is in Alpha stages of development and testing, so it may or may not work properly yet.

## Requirements

- Python 3.7 or higher
- Dragonfly2 (install via `pip install dragonfly2`)
- Tkinter (should be included with Python installation)
- PyDirectInput (install via `pip install pydirectinput`)
- Webview (install via `pip install webview`)
- Keyboard (install via `pip install keyboard`)

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/techsavvy42/Captains_Voice_Commander.git
    ```

2. Install dependencies:

    ```sh
    pip install dragonfly2 tkinter pydirectinput webview keyboard
    ```

## Usage

1. Run the main.py script:

    ```sh
    python main.py
    ```

2. Customize your voice commands using the GUI.

3. Speak your voice commands after activating the program.

## Configuration

You can use the application's GUI to add or remove commands, as well as change your settings. You can also back up your settings.json and commands.json files in case you would like to share them or if you ever need to reinstall. You will be able to keep all your commands and settings intact.

## Example Commands

![Alt text](https://i.imgur.com/BznMYOG.png)

## Known Issues

- The speech recognition may not be 100% accurate in all environments. Adjustments to the microphone sensitivity or environment may be necessary for optimal performance. You can also train your voice using the Windows voice speech recognition on your computer; this can help as well.
- The browser function is in testing and quite buggy right now and not fully implemented, so use it at your own risk. It may or may not work for you.
- The program CURRENTLY only supports a single keybind per voice command. I will be working on adding multi keybinds in the future so that you can do commands such as Alt + F for example. Eventually full on support for chain commands such as 'Alt + F*1.0 second delay*Alt + S*1.0 second delay*Alt + B'

## License

This project is licensed under the MIT License - see the [LICENSE](https://www.mit.edu/~amini/LICENSE.md) for details.
