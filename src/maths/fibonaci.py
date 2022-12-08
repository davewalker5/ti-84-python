from iptutils import prompt_for_integer, prompt_for_yes_no
from oututils import print_title, print_list


def fibonacci(n):
    """
    Return a list of the first "n" entries in the Fibonacci series

    :param n: Number of entries to return
    :return: List of the entries
    """
    if not n or n < 1:
        raise ValueError("Cannot calculate the Fibonacci series for less than 1 digit")

    fs = [1, 1]
    for i in range(1, n - 1):
        fs.append(fs[-2] + fs[-1])
    return fs[:n]


def wrapper():
    """
    Wrapper round the Fibonacci series implementation that prompts for user input
    """
    print_title("Fibonacci Series")
    while True:
        # Prompt for a number and if it's < 0 then quit
        number = prompt_for_integer("How many entries?", minimum_value=1)
        if not number:
            break

        # Prompt for all entries or last one only in the output
        final_entry_only = prompt_for_yes_no("Show last entry only?")

        # Calculate and print the series
        series = fibonacci(number)
        if not final_entry_only:
            print_list(series, 10)
        else:
            print("Entry #" + str(number) + " = " + str(series[-1]))


wrapper()
