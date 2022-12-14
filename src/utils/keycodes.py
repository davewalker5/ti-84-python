"""
Prompt for keypresses and report the key code until 2nd + quit is pressed to exit
"""

from ti_system import *

key_code = None
while key_code != 64:
    print("Press a key ", end="")
    key_code = wait_key()
    if key_code != 64:
        print(key_code, chr(key_code))
