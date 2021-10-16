import keyboard
import time
import pynput.mouse as pmouse

DELTA_KB = 0.2
userInputLastTime = 0
def on_press(key):
    print('{0} pressed'.format(key))
    global userInputLastTime
    userInputLastTime = time.time()

# Adds listener to the keyboard 
keyboard.on_press(on_press)
def on_mouse_move(x, y):
    global userInputLastTime
    userInputLastTime = time.time()

def on_click(x, y, button, pressed):
    global userInputLastTime
    userInputLastTime = time.time()

def on_scroll(x, y, dx, dy):
    global userInputLastTime
    userInputLastTime = time.time()

# Adds listener to the mouse
listener = pmouse.Listener(
        on_move=on_mouse_move,
        on_click=on_click,
        on_scroll=on_scroll)
listener.start()

def reset_user_input():
    """
    Ignores user input for a short period of time.
    """
    global userInputLastTime
    userInputLastTime = 0

def is_user_currently_using_keyboard_or_mouse():
    """
    Returns True if the user is currently using the keyboard or mouse.
    """
    global userInputLastTime
    return (time.time() - userInputLastTime) < DELTA_KB