from iptutils import prompt_for_integer, prompt_for_yes_no
from oututils import print_title, print_list
from fibonaci import fibonacci
from os import environ


def main():
    """
    Entry point for the fibonaci series calculator
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


if "DOCBUILD" not in environ:
    main()
