from ti_system import disp_clr


def pad_string(string_to_pad, character, padded_length, pad_left):
    """
    Pad a string

    :param string_to_pad: String to pad
    :param character: Padding character
    :param padded_length: Required length of padded string
    :param pad_left: True to pad to the left, False to pad to the right
    :return: Padded string
    """

    characters_to_add = padded_length - len(string_to_pad)
    if characters_to_add > 0:
        # Calculate the padding required and pad the string, either to the left or right
        padding = character * characters_to_add
        padded_string = padding + string_to_pad if pad_left else string_to_pad + padding
        return padded_string
    else:
        # Already at the requested length or longer
        return string_to_pad


def format_value(value):
    return "%.2f" % value if isinstance(value, float) else str(value)


def build_row(values, column_widths):
    """
    Tabulate a set of values as a table row with given column widths. Floating point
    numbers are formatted to 2 decimal places

    :param values: List of alues to tabulate
    :param column_widths: List of integer column widths to pad each column to
    :return: Table row text
    """
    row = ""
    for i, value in enumerate(values):
        value_string = pad_string(format_value(value), " ", column_widths[i], False)

        if i > 0:
            row = row + " | "

        row = row + value_string[:column_widths[i]]

    return row


def build_separator(column_widths):
    """
    Print the separator between header and table body

    :param column_widths: List of column widths
    :return: Table row text
    """
    row = ""
    max_column = len(column_widths) - 1
    for i, width in enumerate(column_widths):
        extras = 2 if i > 0 else 1
        row = row + ("-" * (width + extras))
        if i < max_column:
            row = row + "+"

    return row


def calculate_column_widths(data, headers):
    widths = []

    for col in range(len(headers)):
        # Start with header width
        max_len = len(str(headers[col]))

        # Compare against all row values in that column
        for row in data:
            value_len = len(str(row[col]))
            if value_len > max_len:
                max_len = value_len

        widths.append(max_len)

    return widths


def build_table(data, headers):
    """
    Tabulate a collection of row data lists

    :param data: List of row data lists to tabulate
    :param headers: List of column headers
    :param column_widths: List of column widths
    """
    column_widths = calculate_column_widths(data, headers)

    rows = [
        build_row(headers, column_widths),
        build_separator(column_widths)
    ]
    
    for row_data in data:
        rows.append(build_row(row_data, column_widths))

    return rows


def print_table(rows):
    """
    Print a table
    
    :param rows: Table rows
    """
    disp_clr()
    for row in rows:
        print(row)
