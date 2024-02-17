Captains Voice Commander
This Python script utilizes Dragonfly, for speech recognition on Windows and pydirectinput for direct input into DirectX games such as starcitizen which this project is original based on and was created for but this program should work for any other program/directX game if you would like.
https://pypi.org/project/dragonfly2/
https://pypi.org/project/PyDirectInput/

Features
Custom Voice Commands: Define your own voice commands and keybindings for controlling your computer.
Wake Word Recognition: Use a wake word (e.g., "Jarvis") to activate voice commands, similar to virtual assistant programs.
Push-to-Talk: Enable push-to-talk functionality for voice commands, ensuring commands are only recognized when a specific key is pressed.
Graphical User Interface: Interact with the program through a simple GUI built with Tkinter, making it easy to add, edit, and delete commands.
open webpages as a voice command such as snareplan or sc-trade-tools(This feature is in Alpha stages of development and testing so it may or may not work so do not count on it to work properly yet.)

Requirements
Python 3.7 or higher
Dragonfly2 (install via pip install dragonfly2)
Tkinter (should be included with Python installation)
pydirectinput (install via pip install pydirectinput)
webview (install via pip install webview)
keyboard (install via pip install keyboard)
Installation
Clone the repository:

sh
Copy code
git clone https://github.com/techsavvy42/Captains_Voice_Commander.git
Install dependencies:

sh
Copy code
pip install dragonfly2 tkinter pydirectinput webview keyboard
Usage
Run the main.py script:

sh
Copy code
python main.py
Customize your voice commands using the GUI.

Speak your voice commands after activating the program.

Configuration
You can use the applications GUI too add or remove commands, as well as change your settings. You can also back up your settings.json and commands.json files incase you would like to share them or if you ever need to reinstall. You will be able to keep all your commands and settings intact.

Example Commands
Example Pictures here:

Known Issues
The speech recognition may not be 100% accurate in all environments. Adjustments to the microphone sensitivity or environment may be necessary for optimal performance. You can also train your voice using the windows voice speech recognition on your computer this can help as well.

The browser function is in testing and quite buggy right now and not fully implemented, So do as you wish with it. As it may or may not work for you.

License
This project is licensed under the MIT License - see the LICENSE file for details.
