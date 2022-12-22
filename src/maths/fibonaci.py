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
