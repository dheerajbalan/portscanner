Port Scanner Tool

This tool is designed to scan ports, perform network sweeps, and check the reachability of hosts. It supports both TCP and UDP port scanning and offers various functionalities such as pinging targets and checking the availability of hosts on a network.
Features

    TCP Port Scanning: Scan specific or all TCP ports on a target URL or IP.
    UDP Port Scanning: Scan specific UDP ports on a target URL or IP.
    Ping Scan: Check if a target IP is reachable.
    Network Sweep: Check for alive hosts in a specified network.
    Open Ports Only: Show only open ports.
    All Ports Scan: Scan all 65535 ports on a target URL or IP.

Prerequisites

    Python 3.x
    ipaddress module (included in Python 3.3+)

Installation

    Clone the repository:

    bash

    git clone <repository_url>
    cd <repository_directory>

Usage
Command Line Arguments

bash

usage: portscanner.py [-h] [-u URL] [-sn] [-o] [-sU [UDP_PORT]] [-p PORT] [-n NETWORK] [-p-]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     use url or ip of the domain to scan
  -sn, --ping           pings the target
  -o, --open            shows only open ports
  -sU [UDP_PORT], --udp [UDP_PORT]
                        use to scan the udp ports
  -p PORT, --port PORT  use any port number to scan
  -n NETWORK, --network NETWORK
                        checks the alive hosts in the network
  -p-, --ports          to check all ports

Examples

    Scan a specific TCP port:

    bash

sudo python3 portscanner.py -u example.com -p 80

Scan all TCP ports:

bash

sudo python3 portscanner.py -u example.com -p-

Ping a target:

bash

sudo python3 portscanner.py -u example.com -sn

Scan a specific UDP port:

bash

sudo python3 portscanner.py -u example.com -sU 53

Check alive hosts in a network:

bash

sudo python3 portscanner.py -n 192.168.1.0/24

Show only open ports:

bash

    sudo python3 portscanner.py -u example.com -o

Output

The tool will print the results of the scan to the console. For example:

bash

Port 80 is open
Port 443 is open
192.168.1.1 is alive
192.168.1.2 is dead

Notes

    Ensure you have the necessary permissions to run this script, as it may require root privileges to perform network scans.
    This tool is intended for educational and ethical purposes only. Unauthorized scanning and network reconnaissance is illegal and unethical.

License

This project is licensed under the MIT License - see the LICENSE file for details.
