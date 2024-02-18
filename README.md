# Captain's Voice Commander

This Python script utilizes Dragonfly for speech recognition on Windows and pydirectinput for direct input into DirectX games, such as Star Citizen, which this project is originally based on and was created for. However, this program should work for any other program/DirectX game if you would like.

This script cuts straight to the point with voice commands. It is extremely fast when you get it set up and going and can feel really intuitive in games. Unlike some of the programs you might find like voice attack that are filled up with data collectors, that may take up extra game resources, such as login and authentication services, or Diagnostic data such as how many times you exectued a command all constantly running and monitoring you and hogging resources. 

I do have plans on adding some more basic features such as overlays and or text to speech that will allow the program to help users determine what command was executed via verbal/visual confirmation. I would like to try and keep the project as low latency as possible from voice command to keypress. So these types of features and others that I might add later like chatGPT or natural sounding text to speech ETC ETC.... Will be done in such a way that users that do not want to use features that may impact performance or latency and prefeer to work offline with the fastest latency possible from spoken command to keypress they can without these features directly impacting the users performance while turned off.

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
Download the windows version here:
[Download for Windows 0.0.1](https://github.com/techsavvy42/Captains_Voice_Commander/raw/0.0.1-Windows/CaptainsVoiceCommander.zip?download=)

OR

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
- The program will not run and will automatically close If their is no microphone plugged into the computer/system. So make sure you have a microphone plugged in or detected in windows.
- You must run the program in admin mode/give it admin privledges otherwise directX games like Star citizen will not respond to key inputs. SO MAKE SURE TO RUN THE PROGRAM AS ADMINISTRAOR

## Important Documents to read

Dragonfly: [https://pypi.org/project/dragonfly2/](https://pypi.org/project/dragonfly2/)
PyDirectInput: [https://pypi.org/project/PyDirectInput/](https://pypi.org/project/PyDirectInput/)

## License

This project is licensed under the MIT License - see the [LICENSE](https://www.mit.edu/~amini/LICENSE.md) for details.
