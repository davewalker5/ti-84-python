from ti_system import wait_key
from iptutils import prompt_for_integer
from ipv4snt import calculate_subnets
from ipv4nths import nth_subnet
from oututils import print_title

KEY_RIGHT = 1
KEY_LEFT = 2
KEY_QUIT = 64


def display_subnets(subnet_mask, subnet_count, first_network, network_bits, subnet_bits):
    """
    Given a set of subnet details, navigate through the details for each subnet implied by those details

    :param subnet_mask: Subnet mask for all the subnets
    :param subnet_count: Number of subnets
    :param first_network: IP address for the first subnet in dotted-decimal notation
    :param network_bits: Number of network bits
    :param subnet_bits: Number of bits in the network bits corresponding to the subnet bits
    """
    i = 1
    while True:
        # Display the details for the current network
        print("-" * 30)
        details = nth_subnet(first_network, network_bits, subnet_bits, i)
        print("Network " + str(i) + "/" + str(subnet_count) + ":")
        print("Network     : " + details["network"])
        print("Subnet Mask : " + subnet_mask)
        print("First       : " + details["first"])
        print("Last        : " + details["last"])
        print("Broadcast   : " + details["broadcast"])

        # Wait for a keypress
        key_code = wait_key()
        if key_code == KEY_QUIT:
            break
        elif key_code == KEY_RIGHT:
            i = i + 1 if i < subnet_count else 1
        elif key_code == KEY_LEFT:
            i = i - 1 if i > 1 else subnet_count


def main():
    """
    Entry point for subnetting calculation and reporting
    """
    print_title("IPv4 Subnet Calculator")
    while True:
        ip_address = input("IP Address? ")
        if not ip_address:
            break

        subnet_mask = input("Subnet Mask? ")
        hosts = prompt_for_integer("Number of Hosts?", 0, None)
        if hosts is None:
            break

        networks = prompt_for_integer("Number of Networks?", 0, None)
        if networks is None:
            break

        print()

        try:
            # Calculate the subnet details
            subnets = calculate_subnets(ip_address, subnet_mask, hosts, networks)
            display_subnets(subnets["subnet_mask"],
                            subnets["subnet_count"],
                            subnets["first_network"],
                            subnets["network_bits"],
                            subnets["subnet_bits"])

        except BaseException as e:
            print(str(e))

        print()


try:
    # Suppress the application if we're building documentation
    from os import environ
    if "DOCBUILD" not in environ:
        main()

except ImportError:
    # Likely to be running on the calculator so run the application
    main()
