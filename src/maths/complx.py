from strutils import truncate_string


class Complex:
    def __init__(self, real, imaginary, places=2):
        self._real = round(real, places)
        self._imaginary = round(imaginary, places)
        self._places = places

    @property
    def real(self):
        return self._real

    @property
    def imaginary(self):
        return self._imaginary

    def __str__(self):
        symbol = "+" if self._imaginary >= 0 else ""
        return truncate_string(self._real, self._places) + symbol + \
            truncate_string(self._imaginary, self._places) + "i"
