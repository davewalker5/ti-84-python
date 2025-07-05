def subnet_for_hosts(network_bits, number_of_hosts):
    """
    Given a number of hosts, calculate the number of network bits and the number of subnet bits
    required to accommodate that many hosts per subnet

    :param network_bits: Current number of network bits
    :param number_of_hosts: Number of hosts per subnet
    :return: Tuple of the number of network bits and subnet bits
    """
    number_of_subnet_bits = 0
    new_network_bits = 0

    for n in range(1, 33):
        number_of_hosts_for_n = pow(2, n) - 2
        if number_of_hosts_for_n >= number_of_hosts:
            new_network_bits = 32 - n
            number_of_subnet_bits = new_network_bits - network_bits
            break

    return new_network_bits, number_of_subnet_bits


def subnet_for_networks(network_bits, number_of_networks):
    """
    Given a number of networks and current network bits, calculate the number of network bits and subnet
    bits required to accommodate that many subnets

    :param network_bits: Current number of network bits
    :param number_of_networks: Number of subnets required
    :return: Tuple of the number of network bits and subnet bits
    """
    number_of_subnet_bits = 0
    new_network_bits = 0

    for n in range(0, 32):
        number_of_networks_for_n = pow(2, n)
        if number_of_networks_for_n >= number_of_networks:
            number_of_subnet_bits = n
            new_network_bits = network_bits + n
            break

    return new_network_bits, number_of_subnet_bits