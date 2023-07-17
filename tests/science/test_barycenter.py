import unittest
from src.science.orbit import calculate_barycenter

SOLAR_MASS = 1.989E30
EARTH_MASS = 5.97E24


class TestLunarCycle(unittest.TestCase):
    def test_calculate_sun_mercury(self):
        mass = 0.33E24
        distance = 57.9E6
        barycenter = calculate_barycenter(distance, mass, SOLAR_MASS)
        self.assertEqual(9.6063, round(barycenter, 4))

    def test_calculate_sun_venus(self):
        mass = 4.87E24
        distance = 108.2E6
        barycenter = calculate_barycenter(distance, mass, SOLAR_MASS)
        self.assertEqual(264.9234, round(barycenter, 4))

    def test_calculate_sun_earth(self):
        distance = 149.6E6
        barycenter = calculate_barycenter(distance, EARTH_MASS, SOLAR_MASS)
        self.assertEqual(449.0243, round(barycenter, 4))

    def test_calculate_sun_mars(self):
        mass = 0.642E24
        distance = 228E6
        barycenter = calculate_barycenter(distance, mass, SOLAR_MASS)
        self.assertEqual(73.5927, round(barycenter, 4))

    def test_calculate_sun_jupiter(self):
        mass = 1898E24
        distance = 778.5E6
        barycenter = calculate_barycenter(distance, mass, SOLAR_MASS)
        self.assertEqual(742174.1345, round(barycenter, 4))

    def test_calculate_sun_saturn(self):
        mass = 568E24
        distance = 1432E6
        barycenter = calculate_barycenter(distance, mass, SOLAR_MASS)
        self.assertEqual(408820.4072, round(barycenter, 4))

    def test_calculate_sun_uranus(self):
        mass = 86.8E24
        distance = 2867E6
        barycenter = calculate_barycenter(distance, mass, SOLAR_MASS)
        self.assertEqual(125110.4778, round(barycenter, 4))

    def test_calculate_sun_neptune(self):
        mass = 102E24
        distance = 4515E6
        barycenter = calculate_barycenter(distance, mass, SOLAR_MASS)
        self.assertEqual(231526.5884, round(barycenter, 4))

    def test_calculate_earth_moon(self):
        mass = 0.073E24
        distance = 0.384E6
        barycenter = calculate_barycenter(distance, mass, EARTH_MASS)
        self.assertEqual(4638.7556, round(barycenter, 4))
