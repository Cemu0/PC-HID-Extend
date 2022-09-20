from pynput import mouse
# from pynput.mouse import Button, Controller
import pyautogui

screen_w, screen_h = pyautogui.size()
vx = 0
vy = 0

def on_move(x, y):
    print('Pointer moved to {0}'.format(
        (x, y)))
    # mouse.position = (x, y)
    listener.suppress_event()
    

def on_click(x, y, button, pressed):
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))
    if not pressed:
        # Stop listener
        return False

def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up',
        (x, y)))

# Collect events until released
with mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll, suppress = False) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
# listener = mouse.Listener(
#     on_move=on_move,
#     on_click=on_click,
#     on_scroll=on_scroll,
#     suppress = False)
# listener.start()

from time import sleep

sleep(1000)