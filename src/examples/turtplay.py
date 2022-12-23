from turtdraw import TurtleDraw


def playback():
    """
    Use the TurtleDraw implementation to play a set of instructions
    """
    td = TurtleDraw()
    td.play_string("LUURRDDL")


try:
    # Suppress the application if we're building documentation
    from os import environ
    if "DOCBUILD" not in environ:
        playback()

except ImportError:
    # Likely to be running on the calculator so run the application
    playback()
