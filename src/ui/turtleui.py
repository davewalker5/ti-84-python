from turtdraw import TurtleDraw
from os import environ


def main():
    """
    Entry point for the interactive Turtle application
    """
    td = TurtleDraw()
    td.event_loop()


if "DOCBUILD" not in environ:
    main()
