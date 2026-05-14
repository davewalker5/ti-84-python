from ti_system import store_string, recall_string

SEPARATOR = "|"


def encode(data):
    """
    Encode a dictionary of values for string storage

    :param data: Dictionary of simple values to store
    :return: Encoded string for storage
    """
    parts = []
    for k in data:
        parts.append(str(k) + "=" + str(data[k]))

    return SEPARATOR.join(parts)


def decode(text):
    """
    Decode a string from storage format to a simple dictionary of values

    :param text: Encoded string
    :return: Dictionary of decoded values
    """
    data = {}
    if text == "":
        return data
    for part in text.split(SEPARATOR):
        k, v = part.split("=")
        data[k] = v
    return data


def save(slot, data):
    """
    Save a dictionary of simple values

    :param slot: String name
    :param data: Dictionary of simple values to store
    """
    name = "SAVE" + str(slot)
    encoded = encode(data)
    store_string(name, encoded)


def load(slot):
    """
    Retrieve a dictionary of simple values from storage

    :param slot: String name
    :return: Dictionary of simple values
    """
    name = "SAVE" + str(slot)
    text = recall_string(name)
    return decode(text) if text else None
