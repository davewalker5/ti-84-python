from ipv4nwk import network_properties
from oututils import print_title


def main():
    """
    Entry point for network details calculation and reporting
    """
    print_title("IPv4 Network Details")
    while True:
        ip_address = input("IP Address? ")
        if not ip_address:
            break

        subnet_mask = input("Subnet Mask? ")

        print()
        try:
            details = network_properties(ip_address, subnet_mask)

            print("Network   : " + details["network"])
            print("Subnet    : " + details["subnet"])
            print("First     : " + details["first"])
            print("Last      : " + details["last"])
            print("Broadcast : " + details["broadcast"])
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
