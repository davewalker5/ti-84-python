from strutils import pad_string


def get_network_bits(ip_address, subnet_mask):
    """
    Given an IP address and subnet mask, return the number of network bits

    :param ip_address: IP address in dotted-decimal notation, with optional /n suffix
    :param subnet_mask: Subnet mask in dotted-decimal notation, or none if the IP address has the /n suffix
    :return: Tuple of the IP address without the /n suffix and the number of network bits
    """

    # If the IP address is in CIDR format with a /n at the end, extract the number of
    # network bytes from that
    separator_position = ip_address.find("/")
    if separator_position > -1:
        network_bits = int(ip_address[separator_position + 1:])
        ip_address = ip_address[:separator_position]
    else:
        # Calculate the number of network bits from the subnet mask
        subnet_octets = [int(o) for o in subnet_mask.split(".")]
        network_bits = 0
        for octet in subnet_octets:
            if octet == 255:
                network_bits = network_bits + 8
            else:
                binary = pad_string(bin(octet).replace("0b", ""), "0", 8, True)
                network_bits = network_bits + binary.find("0")
                break

    return ip_address, network_bits


def calculate_octets(octets, network_bits, which_address):
    """
    Given an IP address and a number of network bits, calculate the IP address for the
    network, first/last host or broadcast address

    :param octets: List of decimal octets representing the IP address
    :param network_bits: Number of network bits
    :param which_address: AddressType enumeration specifying which address is required
    :return: Tuple of decimal and binary octets for the requested address
    """
    # Convert the IP address represented by the octets into a non-delimited binary string
    binary_octets = []
    for octet in octets:
        binary = pad_string(bin(octet).replace("0b", ""), "0", 8, True)
        binary_octets.append(binary)

    binary_string = "".join(binary_octets)

    # Calculate the binary representation of the required address based on which address is
    # being requested (network, first host, last host or broadcast)
    if which_address == 0:
        binary_ip_string = binary_string[:network_bits] + "0" * (32 - network_bits)
    elif which_address == 1:
        binary_ip_string = binary_string[:network_bits] + "0" * (31 - network_bits) + "1"
    elif which_address == 2:
        binary_ip_string = binary_string[:network_bits] + "1" * (31 - network_bits) + "0"
    elif which_address == 3:
        binary_ip_string = binary_string[:network_bits] + "1" * (32 - network_bits)
    else:
        raise ValueError(str(which_address) + " is not a valid address type")

    # Convert the binary string to decimal and binary octets
    network_octets = []
    for i in range(0, 4):
        binary_octet = binary_ip_string[i * 8:i * 8 + 8]
        network_octets.append(int(binary_octet, 2))

    return network_octets
