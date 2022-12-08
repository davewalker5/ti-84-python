def pad_string(string_to_pad, character, padded_length, pad_left):
    """
    Pad a string

    :param string_to_pad: String to pad
    :param character: Padding character
    :param padded_length: Required length of padded string
    :param pad_left: True to pad to the left, False to pad to the right
    :return: Padded string
    """
    if not string_to_pad:
        raise ValueError("String to pad is empty")

    if not character:
        raise ValueError("Padding character is empty")

    if padded_length < 1:
        raise ValueError("Padding length must be > 0")

    characters_to_add = padded_length - len(string_to_pad)
    if characters_to_add > 0:
        # Calculate the padding required and pad the string, either to the left or right
        padding = character * characters_to_add
        padded_string = padding + string_to_pad if pad_left else string_to_pad + padding
        return padded_string
    else:
        # Already at the requested length or longer
        return string_to_pad
