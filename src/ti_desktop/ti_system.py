from platform import system
_OS = system().casefold()

if _OS in ["windows", "darwin"]:
    from pynput import keyboard
    from pynput.keyboard import Key

    #: Mapping between Pynput keystrokes and TI key codes
    #: Only those mappings needed to support the apps in this repo are represented
    KEY_CODE_MAP = {
        Key.right: 1,
        Key.left: 2,
        Key.up: 3,
        Key.down: 4,
        "p": 150,
        "P": 150,
        "h": 132,
        "H": 132,
        Key.backspace: 9,
        Key.esc: 64
    }

_key = None


def on_press_key(key):
    """
    Pynput key press handler

    :param key: Key that's been pressed
    """
    global _key
    try:
        _key = key.char
    except AttributeError:
        _key = key


def on_release_key(_):
    """
    Pynput key release handler

    :param _: Key that's been released (ignored)
    :return: Always returns False, to break out of the listener
    """
    return False


def wait_key():
    """
    Wait for a keypress and map it to the set of TI key codes supported by this module

    :return: TI key code
    """
    global _OS
    if _OS in ["windows", "darwin"]:
        # Note that on MacOS, if this application is run in e.g. PyCharm then PyCharm needs to be
        # added to the "Accessibility" settings under System Settings
        with keyboard.Listener(on_press=on_press_key, on_release=on_release_key, suppress=True) as listener:
            listener.join()

        # Map the desktop keycode to the set of configured TI-84 key codes
        global _key
        ti_keycode = KEY_CODE_MAP[_key] if _key in KEY_CODE_MAP.keys() else None
        return ti_keycode
    else:
        return None
