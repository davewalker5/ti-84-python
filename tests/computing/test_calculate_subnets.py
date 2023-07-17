import unittest
from src.computing.ipv4snt import calculate_subnets
from src.computing.ipv4nths import nth_subnet


class TestCalculateSubnets(unittest.TestCase):
    def test_calculate_subnets_for_hosts_with_suffix(self):
        subnets = calculate_subnets("10.1.1.0/24", None, 14, 0)
        self.assertEqual(16, subnets["subnet_count"])
        self.assertEqual(28, subnets["network_bits"])
        self.assertEqual("255.255.255.240", subnets["subnet_mask"])

    def test_calculate_subnets_for_hosts_without_suffix(self):
        subnets = calculate_subnets("10.1.1.0", "255.255.255.0", 14, 0)
        self.assertEqual(16, subnets["subnet_count"])
        self.assertEqual(28, subnets["network_bits"])
        self.assertEqual("255.255.255.240", subnets["subnet_mask"])

    def test_calculate_subnets_for_networks_with_suffix(self):
        subnets = calculate_subnets("10.128.192.0/18", None, 0, 30)
        self.assertEqual(32, subnets["subnet_count"])
        self.assertEqual(23, subnets["network_bits"])
        self.assertEqual("255.255.254.0", subnets["subnet_mask"])

    def test_calculate_subnets_for_networks_without_suffix(self):
        subnets = calculate_subnets("10.128.192.0", "255.255.192.0", 0, 30)
        self.assertEqual(32, subnets["subnet_count"])
        self.assertEqual(23, subnets["network_bits"])
        self.assertEqual("255.255.254.0", subnets["subnet_mask"])

    def test_get_subnet_details_for_networks_with_suffix(self):
        subnets = calculate_subnets("192.168.1.0/24", None, 0, 4)
        details = nth_subnet(subnets["first_network"], subnets["network_bits"], subnets["subnet_bits"], 3)
        self.assertEqual("192.168.1.128/26", details["network"])
        self.assertEqual("192.168.1.129", details["first"])
        self.assertEqual("192.168.1.190", details["last"])
        self.assertEqual("192.168.1.191", details["broadcast"])

    def test_get_subnet_details_for_networks_without_suffix(self):
        subnets = calculate_subnets("192.168.1.0", "255.255.255.0", 0, 4)
        details = nth_subnet(subnets["first_network"], subnets["network_bits"], subnets["subnet_bits"], 3)
        self.assertEqual("192.168.1.128/26", details["network"])
        self.assertEqual("192.168.1.129", details["first"])
        self.assertEqual("192.168.1.190", details["last"])
        self.assertEqual("192.168.1.191", details["broadcast"])

    def test_invalid_hosts_error(self):
        with self.assertRaises(ValueError):
            _ = calculate_subnets("10.1.1.0/24", None, -1, 0)

    def test_invalid_networks_error(self):
        with self.assertRaises(ValueError):
            _ = calculate_subnets("10.1.1.0/24", None, 0, -1)

    def test_no_hosts_or_networks_error(self):
        with self.assertRaises(ValueError):
            _ = calculate_subnets("10.1.1.0/24", None, 0, 0)

    def test_hosts_and_networks_error(self):
        with self.assertRaises(ValueError):
            _ = calculate_subnets("10.1.1.0/24", None, 10, 10)

    def test_too_many_hosts_error_with_suffix(self):
        with self.assertRaises(ValueError):
            _ = calculate_subnets("10.1.1.0/24", None, 1000000, 0)

    def test_too_many_hosts_error_without_suffix(self):
        with self.assertRaises(ValueError):
            _ = calculate_subnets("10.1.1.0", "255.255.255.0", 1000000, 0)

    def test_too_many_networks_error_with_suffix(self):
        with self.assertRaises(ValueError):
            _ = calculate_subnets("10.1.1.0/24", None, 0, 1000000)

    def test_too_many_networks_error_without_suffix(self):
        with self.assertRaises(ValueError):
            _ = calculate_subnets("10.1.1.0", "255.255.255.0", 0, 1000000)

    def test_subnet_number_too_small_error_with_suffix(self):
        with self.assertRaises(ValueError):
            subnets = calculate_subnets("192.168.1.0/24", None, 0, 4)
            _ = nth_subnet(subnets["first_network"], subnets["network_bits"], subnets["subnet_bits"], 0)

    def test_subnet_number_too_small_error_without_suffix(self):
        with self.assertRaises(ValueError):
            subnets = calculate_subnets("192.168.1.0", "255.255.255.0", 0, 4)
            _ = nth_subnet(subnets["first_network"], subnets["network_bits"], subnets["subnet_bits"], 0)

    def test_subnet_number_too_large_error_with_suffix(self):
        with self.assertRaises(ValueError):
            subnets = calculate_subnets("192.168.1.0/24", None, 0, 4)
            _ = nth_subnet(subnets["first_network"], subnets["network_bits"], subnets["subnet_bits"], 10000)

    def test_subnet_number_too_large_error_without_suffix(self):
        with self.assertRaises(ValueError):
            subnets = calculate_subnets("192.168.1.0", "255.255.255.0", 0, 4)
            _ = nth_subnet(subnets["first_network"], subnets["network_bits"], subnets["subnet_bits"], 10000)
