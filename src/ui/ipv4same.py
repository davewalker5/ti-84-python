from ipv4snt import same_subnet
from oututils import print_title


def main():
    """
    Entry point for checking if two IPs are on the same subnet
    """
    print_title("IPv4 Same Subnet")
    while True:
        ip_address_1 = input("IP Address 1? ")
        if not ip_address_1:
            break

        ip_address_2 = input("IP Address 2? ")
        if not ip_address_2:
            break

        subnet_mask = input("Subnet Mask? ")
        print()

        try:
            on_same_subnet = same_subnet(ip_address_1, ip_address_2, subnet_mask)
            print("First IP    : " + ip_address_1)
            print("Second IP   : " + ip_address_2)
            print("Subnet Mask : " + subnet_mask)
            print("Same Subnet : " + ("Yes" if on_same_subnet else "No"))

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
