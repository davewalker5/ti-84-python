from turtdraw import TurtleDraw


def main():
    """
    Entry point for the interactive Turtle application
    """
    td = TurtleDraw()
    td.event_loop()


try:
    # Suppress the application if we're building documentation
    from os import environ
    if "DOCBUILD" not in environ:
        main()

except ImportError:
    # Likely to be running on the calculator so run the application
    main()
