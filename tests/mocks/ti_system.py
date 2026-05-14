"""
Mock of the ti_system package providing sufficient stub methods to support the applications
in this repository
"""

STRINGS = {}


def wait_key():
    return None


def store_string(name, value):
    STRINGS[name] = value


def recall_string(name):
    return STRINGS[name]
