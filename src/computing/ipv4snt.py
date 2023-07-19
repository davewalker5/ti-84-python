from ipv4lib import get_network_bits, calculate_octets
from ipv4bits import subnet_for_networks, subnet_for_hosts


def calculate_subnets(ip_address, subnet_mask, number_of_hosts, number_of_networks):
    """
    Given an IP address and a subnet mask, both in dotted decimal format, along with a number of hosts or
    networks, subnet the IP address into either the specified number of subnets or a set of subnets
    accommodating the specified number of hosts

    :param ip_address: IP address string in dotted-decimal notation, optionally with the /n suffix
    :param subnet_mask: Subnet mask string in dotted-decimal notation, or none if the IP address has the /n suffix
    :param number_of_hosts: Number of hosts per network or 0 if subnetting for a number of networks
    :param number_of_networks: Number of subnets required or 0 if subnetting to accommodate a number of hosts
    :return: Dictionary of subnetting properties
    """
    # Validate the requested number of hosts/networks
    if number_of_hosts < 0:
        raise ValueError(str(number_of_hosts) + " is not valid for the number of hosts")

    if number_of_networks < 0:
        raise ValueError(str(number_of_networks) + " is not valid for the number of networks")

    if number_of_hosts == 0 and number_of_networks == 0:
        raise ValueError("Must specify a number of hosts or a number of networks")

    if number_of_hosts > 0 and number_of_networks > 0:
        raise ValueError("Cannot specify both a number of hosts and a number of networks")

    # Get the IP address and number of network bits
    ip_address, network_bits = get_network_bits(ip_address, subnet_mask)

    # Calculate the number of bits we need to take from the host portion
    if number_of_hosts > 0:
        new_network_bits, number_of_subnet_bits = subnet_for_hosts(network_bits, number_of_hosts)
    else:
        new_network_bits, number_of_subnet_bits = subnet_for_networks(network_bits, number_of_networks)

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
