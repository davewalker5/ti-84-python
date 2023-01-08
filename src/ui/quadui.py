from iptutils import prompt_for_float
from oututils import print_title, print_list
from strutils import truncate_string
from quadrat import quadratic_roots


def main():
    """
    Entry point for the quadratic root calculator
    """
    print_title("Quadratic Roots")

    while True:
        a = prompt_for_float("a")
        if a is None:
            return

        b = prompt_for_float("b")
        if b is None:
            return

        c = prompt_for_float("c")
        if c is None:
            return

        roots, are_complex = quadratic_roots(a, b, c, 3)

        results = [str(r) if are_complex else truncate_string(r, 3) for r in roots]
        print("\nQuadratic Roots:\n")
        print_list(results)
        print()


try:
    # Suppress the application if we're building documentation
    from os import environ
    if "DOCBUILD" not in environ:
        main()

except ImportError:
    # Likely to be running on the calculator so run the application
    main()
