from ipv4lib import calculate_octets
from strutils import pad_string


def nth_subnet(first_network_ip_address, network_bits, subnet_bits, n):
    """
    Given a set of subnet details, calculate and return the details for the n'th subnet implied by those details

    :param first_network_ip_address: IP address for the 1st subnet in dotted-decimal notation
    :param network_bits: Number of network bits
    :param subnet_bits: Number of bits in the network bits corresponding to the subnet bits
    :param n: Number of the network for which to calculate details in the range 1 to 2^subnet_bits
    :return: Dictionary of IP addresses for the subnet in dotted-decimal notation
    """
    # Validate the requested number of hosts/networks
    if n < 1 or n > pow(2, subnet_bits):
        raise ValueError(str(n) + "is not valid for the subnet number")

    # Split the address into octets, get the binary version of those octets and generate a non-delimited binary
    # string representing the IP address
    octets = [int(o) for o in first_network_ip_address.split(".")]
    binary_octets = []
    for octet in octets:
        binary = pad_string(bin(octet).replace("0b", ""), "0", 8, True)
        binary_octets.append(binary)

    binary_ip_address = "".join(binary_octets)

    # They're the "n" bits starting at network_bits + 1: Generate a binary IP address string
    # with this combination in the subnet bits and 0 in the host bits
    subnet_portion = pad_string(bin(n - 1).replace("0b", ""), "0", subnet_bits, True)
    subnet_binary_string = binary_ip_address[:network_bits - subnet_bits] + subnet_portion + "0" * (32 - network_bits + subnet_bits)

    # Convert back to a set of octets
    subnet_octets = []
    for i in range(0, 4):
        binary_octet = subnet_binary_string[i * 8:i * 8 + 8]
        subnet_octets.append(int(binary_octet, 2))

    # Calculate each of the addresses based on the IP and number of network
    network_address = ".".join([str(o) for o in calculate_octets(subnet_octets, network_bits, 0)]) + "/" + str(network_bits)
    first_address = ".".join([str(o) for o in calculate_octets(subnet_octets, network_bits, 1)])
    last_address = ".".join([str(o) for o in calculate_octets(subnet_octets, network_bits, 2)])
    broadcast = ".".join([str(o) for o in calculate_octets(subnet_octets, network_bits, 3)])

    return {
        "network": network_address,
        "first": first_address,
        "last": last_address,
        "broadcast": broadcast
    }
