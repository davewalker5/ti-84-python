from ipv4lib import get_network_bits, calculate_octets
from ipv4bits import subnet_for_networks, subnet_for_hosts
from strutils import pad_string


def calculate_subnets(ip_address, subnet_mask=None, number_of_hosts=0, number_of_networks=0, number_of_network_bits=0):
    """
    Given an IP address and a subnet mask, both in dotted decimal format, along with a number of hosts,
    networks or network bits, subnet the IP address into either the specified number of subnets or a set
    of subnets accommodating the specified number of hosts

    :param ip_address: IP address string in dotted-decimal notation, optionally with the /n suffix
    :param subnet_mask: Subnet mask string in dotted-decimal notation, or none if the IP address has the /n suffix
    :param number_of_hosts: Number of hosts per network or 0
    :param number_of_networks: Number of subnets required or 0
    :param number_of_network_bits: Number of network bits in the subnets or 0
    :return: Dictionary of subnet details
    """

    # Validate the requested number of hosts/networks
    if number_of_hosts < 0:
        raise ValueError(str(number_of_hosts) + " is not valid for the number of hosts")

    if number_of_networks < 0:
        raise ValueError(str(number_of_networks) + " is not valid for the number of networks")

    if number_of_network_bits < 0:
        raise ValueError(str(number_of_network_bits) + " is not valid for the number of network bits")

    number_of_parameters = len([i for i in [number_of_hosts, number_of_networks, number_of_network_bits] if i > 0])
    if number_of_parameters < 1:
        raise ValueError("Must specify a number of hosts, a number of networks or a number of network bits")

    if number_of_parameters > 1:
        raise ValueError("Must specify only one of a number of hosts, a number of networks or a number of network bits")

    # Get the IP address and number of network bits
    ip_address, network_bits = get_network_bits(ip_address, subnet_mask)

    # Calculate the number of bits we need to take from the host portion
    if number_of_hosts > 0:
        new_network_bits, number_of_subnet_bits = subnet_for_hosts(network_bits, number_of_hosts)
    elif number_of_networks > 0:
        new_network_bits, number_of_subnet_bits = subnet_for_networks(network_bits, number_of_networks)
    else:
        new_network_bits = number_of_network_bits
        number_of_subnet_bits = new_network_bits - network_bits

    # Calculate the new number of network bits and check it's in range
    if new_network_bits < network_bits or new_network_bits > 32:
        raise ValueError("Subnetting parameters result in an invalid number of network bits")

    # Split the address into octets, get the binary version and generate a non-delimited binary
    # string representing the IP address
    octets = [int(o) for o in ip_address.split(".")]
    network_string = ".".join([str(o) for o in calculate_octets(octets, new_network_bits, 0)])

    # Calculate the subnet mask
    binary_mask_string = "1" * new_network_bits + "0" * (32 - new_network_bits)
    subnet_octets = []
    for i in range(0, 4):
        binary_octet = binary_mask_string[i * 8:i * 8 + 8]
        subnet_octets.append(int(binary_octet, 2))

    subnet_mask = ".".join([str(o) for o in subnet_octets])

    return {
        "network_bits": new_network_bits,
        "subnet_mask": subnet_mask,
        "subnet_bits": number_of_subnet_bits,
        "subnet_count": pow(2, number_of_subnet_bits),
        "first_network": network_string
    }


def same_subnet(ip_address_1, ip_address_2, subnet_mask=None):
    """
    Determine if two IP addresses are on the same subnet

    :param ip_address_1: First IP address in dotted decimal notation with optional /n suffix
    :param ip_address_2: Second IP address in dotted decimal notation with optional /n suffix
    :param subnet_mask: Subnet mask in dotted decimal  (not needed if both IP addresses include /n)
    :return: True/False
    """

    # Parse the two IP addresses to return the IP address without /n suffix and the number of network bits
    ip_address_1, network_bits_1 = get_network_bits(ip_address_1, subnet_mask)
    ip_address_2, network_bits_2 = get_network_bits(ip_address_2, subnet_mask)

    # If the number of network bits aren't the same, they're not on the same subnet
    if network_bits_1 != network_bits_2:
        return False

    # Calculate which octet the network bits end in
    final_network_octet = network_bits_1 // 8
    if final_network_octet % 8 > 0:
        final_network_octet = final_network_octet + 1

    # Split the two IP addresses into octets and then to a non-delimited binary representation
    octets_1 = [int(o) for o in ip_address_1.split(".")]
    octets_2 = [int(o) for o in ip_address_2.split(".")]

    binary_1 = ""
    binary_2 = ""
    for i in range(0, 4):
        binary_1 = binary_1 + pad_string(bin(octets_1[i]).replace("0b", ""), "0", 8, True)
        binary_2 = binary_2 + pad_string(bin(octets_2[i]).replace("0b", ""), "0", 8, True)

    # If the network bits are the same in both, they're on the same subnet
    in_same_subnet = binary_1[:network_bits_1] == binary_2[:network_bits_1]
    return in_same_subnet
