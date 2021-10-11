import keyboard
import mouse
import pyautogui
import time

keyboardPressed = False

def on_press(key):
    global keyboardPressed
    keyboardPressed = True
keyboard.on_press(on_press)

def is_user_currently_using_keyboard_or_mouse():
    """
    Returns True if the user is currently using the keyboard or mouse.
    """
    global keyboardPressed
    keyboardPressedAtStart = keyboardPressed
    keyboardPressed = False

    mousePosBefore = pyautogui.position()
    time.sleep(0.05)
    mousePosAfter = pyautogui.position()

    mouseMoved = (
        mousePosBefore != mousePosAfter
        or
        mouse.is_pressed('left')
        or
        mouse.is_pressed('right')
    )

    keyboardPressedAtEnd = keyboardPressed
    keyboardPressed = False
    
    return keyboardPressedAtStart or keyboardPressedAtEnd or mouseMoved