import pyautogui
import json
import os
import subprocess
import time

COMMANDS_FILE = "config/gesture_commands.json"

# Ensure directory exists
os.makedirs("config", exist_ok=True)

# Load or create gesture-command mapping file
if not os.path.exists(COMMANDS_FILE):
    with open(COMMANDS_FILE, "w") as f:
        json.dump({}, f)  # No default commands

# Dictionary to store the last execution time of each gesture
last_execution_time = {}
EXECUTION_THRESHOLD = 1.5  # Time in seconds before executing the same gesture again

def load_commands():
    """Loads the user's gesture-command mappings."""
    with open(COMMANDS_FILE, "r") as f:
        return json.load(f)


def execute_command(gesture_name):
    """Executes system commands based on recognized gesture with threshold time."""
    global last_execution_time
    commands = load_commands()
    current_time = time.time()
    
    if gesture_name in commands:
        if gesture_name in last_execution_time and (current_time - last_execution_time[gesture_name]) < EXECUTION_THRESHOLD:
            return  # Skip execution if within threshold time
        
        last_execution_time[gesture_name] = current_time
        action = commands[gesture_name]
        print(f"Executing: {action}")
        
        try:
            # Handle system actions (keyboard shortcuts)
            if action in ["volumeup", "volumedown", "right", "left","ok","space"]:
                if action == "volumeup":
                    pyautogui.press("volumeup")
                    pyautogui.press("volumeup")
                    pyautogui.press("volumeup")

                elif action == "volumedown":
                    pyautogui.press("volumedown")
                    pyautogui.press("volumedown")
                    pyautogui.press("volumedown")                                        
                elif action == "right":
                    pyautogui.press("right")  
                elif action == "left":
                    pyautogui.press("left")
                elif action == "ok":
                    pyautogui.press("enter")
                elif action == "space":
                    pyautogui.press(" ")
                elif action == "fist":
                    pass   
            else:
                # Assume it's a CMD command and execute it
                subprocess.run(action, shell=True)
        except Exception as e:
            print(f"Error executing command: {e}")
    else:
        print("Gesture not mapped to any command.")


def add_custom_command(gesture_name, command):
    """Allows users to map gestures to system commands or CMD commands dynamically."""
    commands = load_commands()
    commands[gesture_name] = command

    with open(COMMANDS_FILE, "w") as f:
        json.dump(commands, f)

    print(f"Custom command added: {gesture_name} -> {command}")


def delete_custom_command(gesture_name):
    """Deletes a gesture-to-command mapping."""
    commands = load_commands()
    
    if gesture_name in commands:
        del commands[gesture_name]
        with open(COMMANDS_FILE, "w") as f:
            json.dump(commands, f)
        print(f"Deleted mapping for gesture: {gesture_name}")
    else:
        print(f"Gesture '{gesture_name}' not found in mappings.")

if __name__ == "__main__":
    while True:
        print("\n1. Add Custom Gesture Command")
        print("2. Show Gesture Commands")
        print("3. Delete Gesture Command")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            gesture_name = input("Enter Gesture Name: ")
            command = input("Enter Command to Execute (System or CMD Command): ")
            add_custom_command(gesture_name, command)
        elif choice == "2":
            print(json.dumps(load_commands(), indent=4))
        elif choice == "3":
            gesture_name = input("Enter Gesture Name to Delete: ")
            delete_custom_command(gesture_name)
        elif choice == "4":
            break
