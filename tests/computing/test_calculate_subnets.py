import unittest
from src.computing.ipv4snt import calculate_subnets
from src.computing.ipv4nths import nth_subnet


class TestCalculateSubnets(unittest.TestCase):
    def test_calculate_subnets_for_hosts_with_suffix_1(self):
        subnets = calculate_subnets("10.1.1.0/24", number_of_hosts=14)
        self.assertEqual(16, subnets["subnet_count"])
        self.assertEqual(28, subnets["network_bits"])
        self.assertEqual("255.255.255.240", subnets["subnet_mask"])

    def test_calculate_subnets_for_hosts_without_suffix_1(self):
        subnets = calculate_subnets("10.1.1.0", "255.255.255.0", number_of_hosts=14)
        self.assertEqual(16, subnets["subnet_count"])
        self.assertEqual(28, subnets["network_bits"])
        self.assertEqual("255.255.255.240", subnets["subnet_mask"])

    def test_calculate_subnets_for_hosts_with_suffix_2(self):
        subnets = calculate_subnets("192.168.1.64/26", number_of_hosts=8)
        assert 4 == subnets["subnet_count"]
        assert 28 == subnets["network_bits"]
        assert "255.255.255.240" == subnets["subnet_mask"]

    def test_calculate_subnets_for_hosts_without_suffix_2(self):
        subnets = calculate_subnets("192.168.1.64", "255.255.255.192", number_of_hosts=8)
        assert 4 == subnets["subnet_count"]
        assert 28 == subnets["network_bits"]
        assert "255.255.255.240" == subnets["subnet_mask"]

    def test_calculate_subnets_for_networks_with_suffix_1(self):
        subnets = calculate_subnets("10.128.192.0/18", number_of_networks=30)
        self.assertEqual(32, subnets["subnet_count"])
        self.assertEqual(23, subnets["network_bits"])
        self.assertEqual("255.255.254.0", subnets["subnet_mask"])

    def test_calculate_subnets_for_networks_without_suffix_1(self):
        subnets = calculate_subnets("10.128.192.0", "255.255.192.0", number_of_networks=30)
        self.assertEqual(32, subnets["subnet_count"])
        self.assertEqual(23, subnets["network_bits"])
        self.assertEqual("255.255.254.0", subnets["subnet_mask"])

    def test_calculate_subnets_for_network_bits_with_suffix_1(self):
        subnets = calculate_subnets("192.168.1.96/28", number_of_network_bits=30)
        self.assertEqual(4, subnets["subnet_count"])
        self.assertEqual(30, subnets["network_bits"])
        self.assertEqual("255.255.255.252", subnets["subnet_mask"])

    def test_calculate_subnets_for_network_bits_without_suffix_1(self):
        subnets = calculate_subnets("192.168.1.96", "255.255.255.240", number_of_network_bits=30)
        self.assertEqual(4, subnets["subnet_count"])
        self.assertEqual(30, subnets["network_bits"])
        self.assertEqual("255.255.255.252", subnets["subnet_mask"])


    def test_get_subnet_details_for_networks_with_suffix_1(self):
        subnets = calculate_subnets("192.168.1.0/24", None, 0, 4)
        details = nth_subnet(subnets["first_network"], subnets["network_bits"], subnets["subnet_bits"], 3)
        self.assertEqual("192.168.1.128/26", details["network"])
        self.assertEqual("192.168.1.129", details["first"])
        self.assertEqual("192.168.1.190", details["last"])
        self.assertEqual("192.168.1.191", details["broadcast"])

    def test_get_subnet_details_for_networks_without_suffix_1(self):
        subnets = calculate_subnets("192.168.1.0", "255.255.255.0", 0, 4)
        details = nth_subnet(subnets["first_network"], subnets["network_bits"], subnets["subnet_bits"], 3)
        self.assertEqual("192.168.1.128/26", details["network"])
        self.assertEqual("192.168.1.129", details["first"])
        self.assertEqual("192.168.1.190", details["last"])
        self.assertEqual("192.168.1.191", details["broadcast"])

    def test_get_subnet_details_for_networks_with_suffix_2(self):
        subnets = calculate_subnets("192.168.1.64/26", None, 8, 0)
        details = nth_subnet(subnets["first_network"], subnets["network_bits"], subnets["subnet_bits"], 2)
        self.assertEqual("192.168.1.80/28", details["network"])
        self.assertEqual("192.168.1.81", details["first"])
        self.assertEqual("192.168.1.94", details["last"])
        self.assertEqual("192.168.1.95", details["broadcast"])

    def test_get_subnet_details_for_networks_without_suffix_2(self):
        subnets = calculate_subnets("192.168.1.64/26", "255.255.255.192", 8, 0)
        details = nth_subnet(subnets["first_network"], subnets["network_bits"], subnets["subnet_bits"], 2)
        self.assertEqual("192.168.1.80/28", details["network"])
        self.assertEqual("192.168.1.81", details["first"])
        self.assertEqual("192.168.1.94", details["last"])
        self.assertEqual("192.168.1.95", details["broadcast"])

    def test_invalid_hosts_error(self):
        with self.assertRaises(ValueError):
            _ = calculate_subnets("10.1.1.0/24", number_of_hosts=-1)

    def test_invalid_networks_error(self):
        with self.assertRaises(ValueError):
            _ = calculate_subnets("10.1.1.0/24", number_of_networks=-1)

    def test_invalid_network_bitss_error(self):
        with self.assertRaises(ValueError):
            _ = calculate_subnets("10.1.1.0/24", number_of_network_bits=-1)

    def test_no_hosts_or_networks_error(self):
        with self.assertRaises(ValueError):
            _ = calculate_subnets("10.1.1.0/24")

    def test_hosts_and_networks_error(self):
        with self.assertRaises(ValueError):
            _ = calculate_subnets("10.1.1.0/24", number_of_hosts=10, number_of_networks=10)

    def test_networks_and_network_bits_error(self):
        with self.assertRaises(ValueError):
            _ = calculate_subnets("10.1.1.0/24", number_of_networks=10, number_of_network_bits=10)

    def test_too_many_hosts_error_with_suffix(self):
        with self.assertRaises(ValueError):
            _ = calculate_subnets("10.1.1.0/24", number_of_hosts=1000000)

    def test_too_many_hosts_error_without_suffix(self):
        with self.assertRaises(ValueError):
            _ = calculate_subnets("10.1.1.0", "255.255.255.0", number_of_hosts=1000000)

    def test_too_many_networks_error_with_suffix(self):
        with self.assertRaises(ValueError):
            _ = calculate_subnets("10.1.1.0/24", number_of_networks=1000000)

    def test_too_many_networks_error_without_suffix(self):
        with self.assertRaises(ValueError):
            _ = calculate_subnets("10.1.1.0", "255.255.255.0", number_of_networks=1000000)

    def test_too_many_network_bits_error_with_suffix(self):
        with self.assertRaises(ValueError):
            _ = calculate_subnets("10.1.1.0/24", number_of_network_bits=1000000)

    def test_too_many_network_bits_error_without_suffix(self):
        with self.assertRaises(ValueError):
            _ = calculate_subnets("10.1.1.0", "255.255.255.0", number_of_network_bits=1000000)

    def test_subnet_number_too_small_error_with_suffix(self):
        with self.assertRaises(ValueError):
            subnets = calculate_subnets("192.168.1.0/24", number_of_networks=4)
            _ = nth_subnet(subnets["first_network"], subnets["network_bits"], subnets["subnet_bits"], 0)

    def test_subnet_number_too_small_error_without_suffix(self):
        with self.assertRaises(ValueError):
            subnets = calculate_subnets("192.168.1.0", "255.255.255.0", number_of_networks=4)
            _ = nth_subnet(subnets["first_network"], subnets["network_bits"], subnets["subnet_bits"], 0)

    def test_subnet_number_too_large_error_with_suffix(self):
        with self.assertRaises(ValueError):
            subnets = calculate_subnets("192.168.1.0/24", number_of_networks=4)
            _ = nth_subnet(subnets["first_network"], subnets["network_bits"], subnets["subnet_bits"], 10000)

    def test_subnet_number_too_large_error_without_suffix(self):
        with self.assertRaises(ValueError):
            subnets = calculate_subnets("192.168.1.0", "255.255.255.0", number_of_networks=4)
            _ = nth_subnet(subnets["first_network"], subnets["network_bits"], subnets["subnet_bits"], 10000)
