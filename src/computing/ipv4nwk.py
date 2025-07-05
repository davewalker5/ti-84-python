from ipv4lib import get_network_bits, calculate_octets


def network_properties(ip_address, subnet_mask):
    """
    Given an IP address and a subnet mask, both in dotted decimal format, return
    the network, first host, last host and broadcast addresses

    :param ip_address: IP address string in dotted-decimal notation, optionally with the /n suffix
    :param subnet_mask: Subnet mask string in dotted-decimal notation, or none if the IP address has the /n suffix
    :return: Dictionary of network addresses
    """
    # Get the IP address and number of network bits
    ip_address, network_bits = get_network_bits(ip_address, subnet_mask)

    # Convert the ip_address into a set of octets
    ip_octets = [int(o) for o in ip_address.split(".")]

    # Calculate each of the addresses based on the IP and number of network
    ip_addresses = {
        "network_bits": network_bits,
        "network": ".".join([str(o) for o in calculate_octets(ip_octets, network_bits, 0)]) + "/" + str(network_bits),
        "first": ".".join([str(o) for o in calculate_octets(ip_octets, network_bits, 1)]),
        "last": ".".join([str(o) for o in calculate_octets(ip_octets, network_bits, 2)]),
        "broadcast": ".".join([str(o) for o in calculate_octets(ip_octets, network_bits, 3)])
    }

    # Calculate the subnet mask
    binary_mask_string = "1" * network_bits + "0" * (32 - network_bits)
    subnet_octets = []
    for i in range(0, 4):
        binary_octet = binary_mask_string[i * 8:i * 8 + 8]
        subnet_octets.append(int(binary_octet, 2))

    ip_addresses["subnet"] = ".".join([str(o) for o in subnet_octets])

    return ip_addresses
