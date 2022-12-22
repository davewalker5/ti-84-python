from strutils import pad_string


def print_title(title):
    """
    Display an application title

    :param title: Application title
    """
    print()
    print("=" * len(title))
    print(title)
    print("=" * len(title))
    print()


def print_list(list_to_print, page_size=None):
    """
    Print a list with list indices

    :param list_to_print: List to print out
    :param page_size: Number of lines per page if the output is to be paginated
    """
    # Calculate the pagination and labelling properties
    number_of_entries = len(list_to_print)
    label_length = len(str(number_of_entries))
    step = page_size if page_size and page_size > 0 and (number_of_entries > page_size) else len(list_to_print)

    # Iterate over the pages
    for page in range(0, number_of_entries, step):
        # Iterate over the entries on this page, accounting for a partial
        # final page
        for entry in range(page, min(page + step, number_of_entries)):
            label = pad_string(str(1 + entry), "0", label_length, True)
            print(label + ": " + str(list_to_print[entry]))

        # If pagination's been requested, prompt before the next page
        if page_size and page < (number_of_entries - step):
            _ = input("Press ENTER for next page")
