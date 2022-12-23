from ti_system import wait_key
from turtle import Turtle


class TurtleDraw(Turtle):
    """
    Interactive Turtle drawing application
    """
    KEY_RIGHT = 1
    KEY_LEFT = 2
    KEY_UP = 3
    KEY_DOWN = 4
    KEY_P = 150
    KEY_H = 132
    KEY_CLEAR = 9
    KEY_QUIT = 64
    STEP_SIZE = 10

    #: Maps letters to the key codes for control presses
    INSTRUCTION_MAP = {
        "R": KEY_RIGHT,
        "L": KEY_LEFT,
        "U": KEY_UP,
        "D": KEY_DOWN,
        "P": KEY_P,
        "H": KEY_H,
        "C": KEY_CLEAR,
        "Q": KEY_QUIT
    }

    def __init__(self):
        super(TurtleDraw, self).__init__()
        self._pen_state = True
        self._history = []

    def reset(self):
        """
        Reset the state of the Turtle but do not clear the history
        """
        self.home()
        self.clear()
        self._pen_state = True

    def move(self, heading, distance):
        """
        Move in the specified direction by the specified distance

        :param heading: Heading in degrees
        :param distance: Distance to move
        """
        self.setheading(heading)
        self.forward(distance)

    def toggle_pen_state(self):
        """
        Toggle the "pen down" state
        """
        self._pen_state = not self._pen_state
        if self._pen_state:
            self.pendown()
        else:
            self.penup()

    @property
    def pen_state(self):
        """
        Return the current state of the pen

        :return: True if the pen is down, False if not
        """
        return self._pen_state

    def replay(self):
        """
        Replay all instructions in the history
        """
        self.reset()
        for key_code in self._history:
            self.handle_key(key_code)

    def handle_key(self, key_code):
        """
        Given a key code, take the action appropriate for that key

        :param key_code: Key code from wait_key
        """
        if key_code == TurtleDraw.KEY_RIGHT:
            self.move(0, TurtleDraw.STEP_SIZE)
        elif key_code == TurtleDraw.KEY_UP:
            self.move(90, TurtleDraw.STEP_SIZE)
        elif key_code == TurtleDraw.KEY_LEFT:
            self.move(180, TurtleDraw.STEP_SIZE)
        elif key_code == TurtleDraw.KEY_DOWN:
            self.move(270, TurtleDraw.STEP_SIZE)
        elif key_code == TurtleDraw.KEY_P:
            self.toggle_pen_state()
        elif key_code == TurtleDraw.KEY_H:  # pragma: no cover
            if self._history:
                self.replay()
        elif key_code == TurtleDraw.KEY_CLEAR:
            self.reset()
            self._history.clear()

    @staticmethod
    def map_key_code_to_character(key_code):
        """
        Map a key code to the corresponding character from the "play_string" instruction set

        :param key_code: Key code to map
        :return: Corresponding character
        """
        return [k for k, v in TurtleDraw.INSTRUCTION_MAP.items()if v == key_code][0]

    @property
    def instructions_string(self):
        """
        Return the current history as an instruction string

        :return: Instructions string suitable for use with play_string
        """
        instructions = "".join(list(map(TurtleDraw.map_key_code_to_character, self._history)))
        return instructions

    def play_string(self, instructions):
        """
        Play the instructions held in the string, mapping each character to the corresponding key code
        before handling it as though entered on the keyboard

        :param instructions: String of instructions entered as regular characters
        """
        for c in instructions.upper():
            try:
                key_code = TurtleDraw.INSTRUCTION_MAP[c]
                if key_code == TurtleDraw.KEY_QUIT:
                    return
                elif key_code != TurtleDraw.KEY_H:  # pragma: no cover
                    self._history.append(key_code)
                self.handle_key(key_code)
            except KeyError:
                pass

        self.event_loop()

    def event_loop(self):
        """
        Event loop : Wait for a key press and respond to that keypress until the user
        hits "2nd, quit"
        """
        self.showturtle()
        while True:
            key_code = wait_key()
            if key_code == TurtleDraw.KEY_QUIT:
                break
            elif key_code != TurtleDraw.KEY_H:  # pragma: no cover
                self._history.append(key_code)
            self.handle_key(key_code)
