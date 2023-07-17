def calculate_barycenter(a, m1, m2):
    """
    Calculate the barycenter for a two-body system

    :param a: Distance between the two bodies
    :param m1: Mass of the first body
    :param m2: Mass of the second body
    """
    return a * min(m1, m2)/(m1 + m2)
