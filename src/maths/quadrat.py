from math import sqrt
from complx import Complex


def quadratic_roots(a, b, c, places):
    """
    Return the roots of a quadratic equation given the numeric coefficients

    :param a: Value for 1st numeric coefficient
    :param b: Value for 2md numeric coefficient
    :param c: Value for 3rd numeric coefficient
    :param places: Number of decimal places to round the resuls to
    :return: Tuple of a list of roots and a boolean indicating whether they're real or complex
    """
    if a == 0:
        raise ValueError("Invalid value for 'a'")

    are_complex = False
    discriminant = b * b - 4 * a * c
    if discriminant == 0:
        # Discriminant is 0, so there's only one root
        root = b / 2 * a
        roots = [round(root, places)]
    elif discriminant > 0:
        # Discriminant is positive, so there are two real roots
        root1 = (b - sqrt(discriminant)) / (2 * a)
        root2 = (b + sqrt(discriminant)) / (2 * a)
        roots = [round(root1, places), round(root2, places)]
    else:
        # Discriminant is negative, so there are two complex roots
        are_complex = True
        real = b / (2 * a)
        imaginary = sqrt(abs(discriminant)) / (2 * a)
        root1 = Complex(real, -imaginary, places)
        root2 = Complex(real, imaginary, places)
        roots = [root1, root2]

    return roots, are_complex

