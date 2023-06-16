import argparse


def init_parser(file_path):
    parser = argparse.ArgumentParser(
        description='Update mappings in hosts file',
        epilog='hosts file location: ' + file_path
    )
    parser.add_argument(
        "-D", "--debug",
        default='0',
        required=False,
        help="Show debug information",
    )
    parser.add_argument(
        "-rn", "--run_nmap",
        default='1',
        required=False,
        help="Run nmap to discover all the 256 devices in the network",
    )
    parser.add_argument(
        "-if", "--input",
        default='hostname_mac.txt',
        required=False,
        help="Input file with hostname and MAC addresses. " +
             "Default: hostname_mac.txt",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-l", "--list", action="store_true",
        help="Show the hostnames, MAC and ip addresses" +
             " for items in the input file"
    )
    group.add_argument("-s", "--show", action="store_true",
                       help="Show the content of hosts file")
    group.add_argument("-c", "--check", metavar='HOSTNAME', nargs='+',
                       help="Check if the host name existed in the host file")
    group.add_argument("-i", "--insert", metavar='HOSTNAME[:IP]', nargs='+',
                       help="Insert HOSTNAME[:IP] mappings")
    group.add_argument("-r", "--remove", metavar='HOSTNAME', nargs='+',
                       help="Remove mapping for HOSTNAME from hosts file.")
    return parser
