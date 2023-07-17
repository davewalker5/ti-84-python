import unittest
from src.computing.ipv4nwk import network_properties


class TestIPv4NetworkAddresses(unittest.TestCase):
    def test_calculate_network_properties(self):
        properties = network_properties("172.16.35.123", "255.255.240.0")
        self.assertEqual("172.16.47.255", properties["broadcast"])
        self.assertEqual("172.16.32.1", properties["first"])
        self.assertEqual("172.16.47.254", properties["last"])
        self.assertEqual("172.16.32.0/20", properties["network"])
        self.assertEqual("255.255.240.0", properties["subnet"])
        self.assertEqual(20, properties["network_bits"])

    def test_calculate_network_properties_cidr(self):
        properties = network_properties("172.16.35.123/20", None)
        self.assertEqual("172.16.47.255", properties["broadcast"])
        self.assertEqual("172.16.32.1", properties["first"])
        self.assertEqual("172.16.47.254", properties["last"])
        self.assertEqual("172.16.32.0/20", properties["network"])
        self.assertEqual("255.255.240.0", properties["subnet"])
        self.assertEqual(20, properties["network_bits"])
