import unittest
from src.computing.ipv4snt import same_subnet


class TestSameSubnet(unittest.TestCase):
    def test_same_subnet_cidr(self):
        are_same_subnet = same_subnet("10.1.255.1/17", "10.1.128.2/17")
        self.assertTrue(are_same_subnet)

    def test_same_subnet_not_cidr(self):
        are_same_subnet = same_subnet("10.1.255.1", "10.1.128.2", "255.255.128.0")
        self.assertTrue(are_same_subnet)

    def test_different_subnet_cidr(self):
        are_same_subnet = same_subnet("10.1.248.1/20", "10.1.192.2/20")
        self.assertFalse(are_same_subnet)

    def test_same_subnet_not_cidr(self):
        are_same_subnet = same_subnet("10.1.248.1", "10.1.192.2", "255.255.240.0")
        self.assertFalse(are_same_subnet)
