import subprocess
import sys
import time
import tkinter as tk
from tkinter import ttk
import json
import pydirectinput
import threading
import os
import webview
import pythoncom
import keyboard
from dragonfly import Grammar, CompoundRule
from dragonfly.engines.backend_sapi5.engine import Sapi5InProcEngine

# Create an instance of the SAPI5 engine
engine = Sapi5InProcEngine()
grammar = Grammar("example grammar")


def update_commands_with_wake_word(commands, old_wake_word, new_wake_word, wake_word_enabled):
    # Remove all occurrences of old wake word from each command
    for command in commands:
        command["command"] = command["command"].replace(old_wake_word, "").strip()

    if wake_word_enabled:
        # Add new wake word to each command
        for command in commands:
            command["command"] = f"{new_wake_word} {command['command']}"

    # Write the modified commands back to the commands.json file
    with open("commands.json", "w") as json_file:
        json.dump(commands, json_file, indent=4)

    return commands


# Update the listbox with commands
def update_listbox():
    # Reset the grammar with the new commands
    reset_grammar(commands, wake_word, wake_word_enabled, selected_microphone, pushto_talk_enabled,
                  selected_pushto_talk_button)
    listbox.delete(0, tk.END)  # Clear the listbox
    for command in commands:
        display_command = command["command"]
        if display_command.lower().startswith(wake_word.lower()):
            display_command = display_command[len(wake_word):].strip()
        listbox.insert(tk.END,
                       f"{display_command}: {command.get('keybind', '')}, Press Time: {command.get('press_time', 0.0)}")


# Save command to JSON file
def save_command():
    command = command_var.get()
    keybind = keybind_var.get()
    press_time = press_time_var.get()

    if command.strip() and keybind.strip() and press_time.strip():
        # Check if the command already exists
        for existing_command in commands:
            if existing_command["command"] == command:
                print("Command with the same name already exists.")
                return

        # Add the wake word if it is enabled
        if wake_word_enabled_var.get():
            command = f"{wake_word} {command}"

        # If the command doesn't exist, add it to the list
        commands.append({"command": command, "keybind": keybind, "press_time": float(press_time)})
        with open("commands.json", "w") as f:
            json.dump(commands, f, indent=4)
        update_listbox()  # Update the listbox with the new command
        # Clear the entry fields after saving
        command_entry.delete(0, tk.END)
        keybind_entry.delete(0, tk.END)
        press_time_entry.delete(0, tk.END)
    else:
        print("Command, keybind, and press time must be provided.")


# Double-click event handler for listbox items
def edit_item(event):
    global dialog_open
    if not dialog_open:
        # Get the index of the selected item
        index = listbox.curselection()
        if index:
            index = int(index[0])
            selected_item = commands[index]
            # Show popup window for editing the selected item
            edit_popup(selected_item, index)
            dialog_open = True


# Function to create a popup window for editing a command
def edit_popup(selected_item, index):
    popup = tk.Toplevel()
    popup.title("Edit Command")

    def close_popup():
        popup.destroy()
        global dialog_open
        dialog_open = False

    # Entry fields for editing the command
    command_var.set(selected_item["command"])
    keybind_var.set(selected_item.get("keybind", ""))
    press_time_var.set(selected_item.get("press_time", 0.0))
    command_label = tk.Label(popup, text="Command:")
    command_label.grid(row=0, column=0)
    command_entry = tk.Entry(popup, textvariable=command_var)
    command_entry.grid(row=0, column=1)

    key_label = tk.Label(popup, text="Key Binding:")
    key_label.grid(row=1, column=0)
    keybind_entry = ttk.Combobox(popup, textvariable=keybind_var, values=available_inputs)
    keybind_entry.grid(row=1, column=1)

    press_time_label = tk.Label(popup, text="Press Time (seconds):")
    press_time_label.grid(row=2, column=0)
    press_time_entry = tk.Entry(popup, textvariable=press_time_var)
    press_time_entry.grid(row=2, column=1)

    # Button to save changes
    save_button = tk.Button(popup, text="Save", command=lambda: save_changes(selected_item, index, popup))
    save_button.grid(row=3, column=0, columnspan=2)

    # Button to delete command
    delete_button = tk.Button(popup, text="Delete", command=lambda: delete_command(selected_item, index, popup))
    delete_button.grid(row=4, column=0, columnspan=2)

    # Button to cancel
    cancel_button = tk.Button(popup, text="Cancel", command=close_popup)
    cancel_button.grid(row=5, column=0, columnspan=2)


# Function to delete the selected command
def delete_command(selected_item, index, popup):
    commands.remove(selected_item)
    with open("commands.json", "w") as f:
        json.dump(commands, f, indent=4)
    update_listbox()  # Update the listbox after deleting the command
    popup.destroy()
    global dialog_open
    dialog_open = False


# Function to save changes made in the popup window
def save_changes(selected_item, index, popup):
    selected_item["command"] = command_var.get()
    selected_item["keybind"] = keybind_var.get()
    selected_item["press_time"] = float(press_time_var.get())
    if wake_word_enabled_var.get():  # Check if wake word is enabled
        # Add wake word to the command
        selected_item["command"] = f"{wake_word} {selected_item['command']}"
    commands[index] = selected_item
    with open("commands.json", "w") as f:
        json.dump(commands, f, indent=4)
    update_listbox()  # Update the listbox with the modified command
    popup.destroy()
    global dialog_open
    dialog_open = False


# Function to save the Wake Word setting to a JSON file
def save_wake_word(wake_word):
    with open("settings.json", "w") as f:
        json.dump({"wake_word": wake_word, "wake_word_enabled": wake_word_enabled_var.get()}, f, indent=4)


def get_available_microphones():
    engine = Sapi5InProcEngine()
    engine.connect()
    audio_sources = engine.get_audio_sources()
    microphones = [source[1] for source in audio_sources]
    return microphones


# Function to load settings including the selected microphone
def load_settings():
    try:
        with open("settings.json") as f:
            settings = json.load(f)
            return (
                settings.get("wake_word", ""),
                settings.get("wake_word_enabled", False),
                settings.get("microphone", None),
                settings.get("pushto_talk_enabled", False),
                settings.get("pushto_talk_button", ""),
            )  # Load the microphone setting
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return "", False, None


def load_wake_word():
    try:
        with open("settings.json") as f:
            settings = json.load(f)
            wake_word = settings.get("wake_word", "")
            wake_word_enabled = settings.get("wake_word_enabled", False)
            pushto_talk_enabled = settings.get("pushto_talk_enabled", False)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        wake_word = ""
        wake_word_enabled = False
        pushto_talk_enabled = False
    return wake_word, wake_word_enabled, pushto_talk_enabled


def load_commands():
    try:
        with open("commands.json") as f:
            commands = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        commands = []
    return commands


# Function to update the Wake Word setting
def update_wake_word():
    global wake_word
    wake_word, wake_word_enabled, pushto_talk_enabled = load_wake_word()
    wake_word_var.set(wake_word)
    wake_word_enabled_var.set(wake_word_enabled)
    pushto_talk_enabled_var.set(pushto_talk_enabled)


def save_custom_commands(commands):
    with open("commands.json", "w") as f:
        json.dump(commands, f, indent=4)


def run_voice_recognition():
    print("Listening for voice commands. Press Ctrl+C to exit.")
    try:
        while True:
            pythoncom.PumpWaitingMessages()
    except KeyboardInterrupt:
        print("\nExiting...")


try:
    with open("commands.json") as f:
        custom_commands = json.load(f)
except (FileNotFoundError, json.decoder.JSONDecodeError):
    custom_commands = {}


def get_available_inputs():
    keyboard_mapping = pydirectinput.KEYBOARD_MAPPING

    # Extract single characters (1-9, a-z) and sort them
    single_chars = sorted(filter(lambda k: len(k) == 1 and k.isalnum(), keyboard_mapping.keys()))

    # Filter out keys to ignore
    keys_to_ignore = ['escape', 'prtscr', 'prtsc', 'prntscrn', 'apps']  # These keys are extra of the same thing.
    valid_keys = [key for key in keyboard_mapping.keys() if key not in keys_to_ignore]

    # Remove duplicates and sort the remaining keys
    remaining_keys = sorted(set(valid_keys) - set(single_chars))

    # Combine the lists while maintaining the desired order
    ordered_keys = single_chars + remaining_keys

    # Add the custom command "Open website url"
    ordered_keys.append("Open website url")
    return ordered_keys


# Example usage
available_inputs = get_available_inputs()
print(available_inputs)


def reload_settings():
    global wake_word, wake_word_enabled, selected_microphone, pushto_talk_enabled, selected_pushto_talk_button
    wake_word, wake_word_enabled, selected_microphone, pushto_talk_enabled, selected_pushto_talk_button = load_settings()


def update_grammar():
    try:
        # Attempt to open the commands.json file
        with open("commands.json", "r") as json_file:
            # Load the commands from the file
            custom_commands = json.load(json_file)
    except FileNotFoundError:
        # If the file is not found, initialize an empty dictionary for custom commands
        custom_commands = {}

    # Check if the grammar rules are structured as expected
    if isinstance(grammar.rules, dict):
        # Get the names of existing rules
        rule_names = grammar.rules.keys()
        # Remove the ExampleRule if it already exists
        if "ExampleRule" in rule_names:
            grammar.remove_rule("ExampleRule")
        # Add the updated ExampleRule with the loaded custom commands and wake word settings
        grammar.add_rule(ExampleRule(custom_commands))
        # Load the grammar
        grammar.load()
    else:
        # Print a message if the grammar rules are not structured as expected
        print("Grammar rules are not structured as expected.")


# In the open_settings_dialog function:
def open_settings_dialog():
    global wake_word, wake_word_enabled, old_wake_word
    dialog = tk.Toplevel(root)
    dialog.title("Settings")
    # Usage
    available_inputs = get_available_inputs()
    # Load microphone options
    available_microphones = get_available_microphones()

    # Variable to track selected microphone
    microphone_var = tk.StringVar()
    input_var = tk.StringVar()
    selected_microphone = load_settings()[2]  # Load the selected microphone
    microphone_var.set(selected_microphone)  # Set initial value based on loaded setting

    selected_pushto_talk_button = load_settings()[4]  # Load the selected microphone
    input_var.set(selected_pushto_talk_button)  # Set initial value based on loaded setting

    def save_settings():
        global wake_word, wake_word_enabled, old_wake_word
        # Assign the current wake word to old_wake_word
        old_wake_word = wake_word
        wake_word = wake_word_entry.get()
        wake_word_enabled = wake_word_enabled_var.get()
        selected_microphone = microphone_var.get()
        selected_pushto_talk_button = input_var.get()
        save_wake_word(wake_word)
        save_microphone(selected_microphone,
                        selected_pushto_talk_button)  # Pass selected microphone to save_microphone function
        update_commands_with_wake_word(commands, old_wake_word, wake_word, wake_word_enabled)
        # Re-run the program with admin rights
        reload_settings()
        update_listbox()
        dialog.destroy()

    wake_word_label = tk.Label(dialog, text="Wake Word:")
    wake_word_label.grid(row=1, column=0)
    wake_word_entry = tk.Entry(dialog, textvariable=wake_word_var)
    wake_word_entry.grid(row=1, column=1)

    # Microphone selection option
    microphone_label = tk.Label(dialog, text="Selected Microphone:")
    microphone_label.grid(row=6, column=0)
    microphone_option = ttk.Combobox(dialog, textvariable=microphone_var, values=available_microphones)
    microphone_option.grid(row=6, column=1)
    # Example of using this in a ttk Combobox

    wake_word_enabled_check = tk.Checkbutton(dialog, text="Enable Wake Word", variable=wake_word_enabled_var)
    wake_word_enabled_check.grid(row=0, column=0, columnspan=2)

    save_button = tk.Button(dialog, text="Save", command=save_settings)
    save_button.grid(row=7, column=0, columnspan=2)

    enable_push_button = tk.Checkbutton(dialog, text="Enable push to talk", variable=pushto_talk_enabled_var)
    enable_push_button.grid(row=2, column=0, columnspan=2)
    # Example of using this in a ttk Combobox
    input_label = tk.Label(dialog, text="Push to talk button")
    input_label.grid(row=3, column=0)
    input_option = ttk.Combobox(dialog, textvariable=input_var, values=available_inputs)
    input_option.grid(row=3, column=1)


# In the save_settings function:
def save_settings(selected_microphone, selected_pushto_talk_button):
    with open("settings.json", "w") as f:
        json.dump(
            {
                "wake_word": wake_word,
                "wake_word_enabled": wake_word_enabled_var.get(),
                "microphone": selected_microphone,  # Save the selected microphone
                "pushto_talk_enabled": wake_word_enabled_var.get(),
                "pushto_talk_button": selected_pushto_talk_button,
            },
            f,
            indent=4,
        )


# Load Wake Word setting and selected microphone
wake_word, wake_word_enabled, selected_microphone, pushto_talk_enabled, selected_pushto_talk_button = load_settings()


def reset_grammar(commands, wake_word, wake_word_enabled, selected_microphone,
                  pushto_talk_enabled, selected_pushto_talk_button):
    global example_rule, grammar
    example_rule = ExampleRule(commands, wake_word, wake_word_enabled, selected_microphone, pushto_talk_enabled,
                               selected_pushto_talk_button)
    grammar.unload()
    grammar = Grammar("example grammar")
    grammar.add_rule(example_rule)
    grammar.load()


# Function to save selected microphone to JSON file
def save_microphone(selected_microphone, selected_pushto_talk_button):
    with open("settings.json", "w") as f:
        json.dump(
            {
                "wake_word": wake_word,
                "wake_word_enabled": wake_word_enabled_var.get(),
                "microphone": selected_microphone,
                "pushto_talk_enabled": pushto_talk_enabled_var.get(),
                "pushto_talk_button": selected_pushto_talk_button,
            },
            f,
            indent=4,
        )


class ExampleRule(CompoundRule):
    def __init__(self, commands, wake_word, wake_word_enabled, selected_microphone,
                 pushto_talk_enabled, selected_pushto_talk_button):
        self.commands = commands
        self.wake_word = wake_word
        self.wake_word_enabled = wake_word_enabled
        self.pushto_talk_enabled = pushto_talk_enabled
        self.selected_pushto_talk_button = selected_pushto_talk_button
        self.selected_microphone = selected_microphone  # Assign the selected microphone
        self.spec = " | ".join(f'"{command["command"]}"' for command in commands)
        super(ExampleRule, self).__init__()

        # Configure the microphone
        self.configure_microphone()

    def configure_microphone(self):

        # Connect to the engine
        engine.connect()

        # Get the available audio sources
        audio_sources = engine.get_audio_sources()

        # If a selected microphone is specified in the settings, use it
        if self.selected_microphone:
            for i, (index, description, handle) in enumerate(audio_sources):
                if description == self.selected_microphone:
                    # Select the audio source
                    engine.select_audio_source(i)
                    break
            else:
                print("Selected microphone not found. Using default microphone.")
        else:
            print("No microphone selected. Using default microphone.")

    def press_and_hold_key(self, keybind, press_time):
        print(f"Pressing and holding key {keybind} for {press_time} seconds")
        pydirectinput.keyDown(keybind)
        time.sleep(press_time)
        pydirectinput.keyUp(keybind)
        print(f"Released key {keybind}")

    def open_webview(self, keybind):
        # Continue with your application logic
        print("Creating webview window...")
        webview.create_window('Captains Voice Commander', keybind)
        try:
            print("Starting webview...")
            webview.start(gui='qt')
            print("Webview started successfully.")
        except Exception as e:
            print("Exception occurred while starting webview:", e)

    def _process_recognition(self, node, extras):
        words = node.words()
        recognized_text = " ".join(words).lower()
        # Check if push-to-talk is enabled and if the push-to-talk button is being pressed
        if self.pushto_talk_enabled and not keyboard.is_pressed(self.selected_pushto_talk_button):
            print("Push-to-talk is enabled. Press and hold the push-to-talk button to issue commands.")
            return

        for command in self.commands:
            if command["command"] in recognized_text:
                print("Voice command spoken:", command["command"])
                keybind = command.get("keybind", "")
                press_time = command.get("press_time", 0.0)
                print(f"Press time for command {command['command']}: {press_time}")
                if keybind:
                    if keybind.startswith("http://") or keybind.startswith("https://"):
                        print("Opening website URL:", keybind)
                        # Call open_webview with the URL
                        self.open_webview(keybind)
                    elif press_time == 0.0:
                        print("Pressing key immediately")
                        pydirectinput.press(keybind)
                    else:
                        print("Starting separate thread for key press")
                        threading.Thread(target=self.press_and_hold_key, args=(keybind, press_time)).start()
                break
        else:
            print("Unrecognized command:", recognized_text)


# Main Tkinter window
root = tk.Tk()
root.title("Captains Voice Commander")

# Load commands from JSON file
commands = load_commands()

# Listbox to display commands
listbox = tk.Listbox(root, width=50, height=10)
listbox.grid(row=0, column=0, columnspan=2)
update_listbox()  # Update the listbox with initial commands
listbox.bind("<Double-Button-1>", edit_item)  # Bind double-click event to listbox items

# Entry fields for new command
command_var = tk.StringVar()
keybind_var = tk.StringVar()
press_time_var = tk.StringVar()


# Removes the wake word from the command box view
def update_command_var(*args):
    display_command = command_var.get()
    if display_command.lower().startswith(wake_word.lower()):
        display_command = display_command[len(wake_word):].strip()
    command_entry.delete(0, tk.END)
    command_entry.insert(0, display_command)


# Trace the variable to call the update_command_var function whenever command_var changes
command_var.trace_add("write", update_command_var)
command_label = tk.Label(root, text="Command:")
command_label.grid(row=1, column=0)
command_entry = tk.Entry(root, textvariable=command_var)
command_entry.grid(row=1, column=1)
available_inputs = get_available_inputs()

key_label = tk.Label(root, text="Key Binding:")
key_label.grid(row=2, column=0)
keybind_entry = ttk.Combobox(root, textvariable=keybind_var, values=available_inputs)
keybind_entry.grid(row=2, column=1)

press_time_label = tk.Label(root, text="Press Time (seconds):")
press_time_label.grid(row=3, column=0)
press_time_entry = tk.Entry(root, textvariable=press_time_var)
press_time_entry.grid(row=3, column=1)

# Button to save command
save_button = tk.Button(root, text="Add New Command", command=save_command)
save_button.grid(row=4, column=0, columnspan=2)

# Variable to track if a dialog box is open
dialog_open = False

wake_word, wake_word_enabled, pushto_talk_enabled = load_wake_word()
old_wake_word = wake_word
wake_word_var = tk.StringVar(value=wake_word)
wake_word_enabled_var = tk.BooleanVar(value=wake_word_enabled)
pushto_talk_enabled_var = tk.BooleanVar(value=pushto_talk_enabled)

# Global variable for microphone option
microphone_option = None

# Set the initial value of the microphone option based on the loaded setting
if microphone_option is not None:
    microphone_option.set(selected_microphone)

# Button to open settings dialog for Wake Word
settings_button = tk.Button(root, text="Settings", command=open_settings_dialog)
settings_button.grid(row=5, column=0, columnspan=2)

root.mainloop()
