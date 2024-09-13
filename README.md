Port Scanner

A versatile port scanning tool written in Python. This script allows you to scan ports on a specified target, check network hosts, and perform ping and UDP scans.
Features

Port Scanning: Scan specific ports or all ports on a target.
Ping Scan: Check if a target is reachable.
UDP Scan: Scan UDP ports.
Network Host Check: Verify if hosts in a given network are alive.
Customizable Workers and Batch Size: Optimize scanning performance based on your system's specs.

Installation

Ensure you have Python 3 installed. You can then clone the repository and run the script directly.

bash

	git clone https://github.com/yourusername/portscanner.git
	cd portscanner

Usage

bash

	python portscanner.py -h

Options

    -h, --help: Show this help message and exit.
    -u URL, --url URL: Use URL or IP of the domain to scan.
    -sn, --ping: Ping the target.
    -o, --open: Show only open ports.
    -sU [UDP_PORT], --udp [UDP_PORT]: Scan UDP ports.
    -p PORT, --port PORT: Scan a specific port.
    -n NETWORK, --network NETWORK: Check alive hosts in the network.
    -p-, --ports: Scan all ports.
    -w WORKERS, --workers WORKERS: Number of concurrent workers.
    -b BATCH_SIZE, --batch-size BATCH_SIZE: Size of each batch for port scanning.

Examples

    Scan all ports on a target URL with custom workers and batch size:

    bash

	python portscanner.py -u example.com -p- --workers 100 --batch-size 8000

Ping a target to check if it is reachable:

bash

	python portscanner.py -u example.com -sn

Scan a specific port on a target URL:

bash

	python portscanner.py -u example.com -p 80

Check alive hosts in a network:

bash

    	python portscanner.py -n 192.168.1.0/24

Optimization
System Specs and Recommendations

4GB RAM: Workers 50-75, Batch Size 2000-5000
6GB RAM: Workers 75-100, Batch Size 5000-8000
8GB RAM: Workers 100-125, Batch Size 8000-12000
16GB RAM: Workers 125-200, Batch Size 12000-20000

License

This project is licensed under the MIT License. See the LICENSE file for details.
