from pynput import keyboard
from pynput.keyboard import Key
import time

altPressed = False

def on_press(key):
    global altPressed
    altPressed = (key == Key.alt_l)
    if key == keyboard.Key.esc:
        keyboardListener.stop()

def win32_event_filter(msg, data):
    global altPressed
    if data.vkCode == 115 and altPressed: # suppress f4 when alt_l pressed
        print("suppressed f4")
        keyboardListener.suppress_event()

def on_release(key):
    global altPressed
    altPressed = (key == Key.alt_l)

keyboardListener = keyboard.Listener(on_press=on_press,  
                                     win32_event_filter=win32_event_filter,
                                     on_release=on_release)

if __name__ == '__main__':
    keyboardListener.start()
    while(keyboardListener.is_alive()):
        time.sleep(1)
