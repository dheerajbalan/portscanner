import socket
import argparse
import subprocess
import ipaddress
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", dest="url", help="use url or ip of the domain to scan")
    parser.add_argument("-sn", "--ping", action="store_true", help="pings the target")
    parser.add_argument("-o", "--open", action="store_true", help="shows only open ports")
    parser.add_argument("-sU", "--udp", dest="udp_port", type=int, nargs='?', const=None, help="use to scan the udp ports")
    parser.add_argument("-p", "--port", type=int, dest="port", help="use any port number to scan")
    parser.add_argument("-n", "--network", dest="network", help="checks the alive hosts in the network")
    parser.add_argument("-p-", "--ports", action="store_true", help="to check all ports")
    return parser.parse_args()

def get_url(url, port):
    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scanner.settimeout(1)
    try:
        conn = scanner.connect_ex((url, port))
        if conn == 0:
            return port, True
        else:
            return port, False
    finally:
        scanner.close()

def ping_scan(url):
    output = subprocess.call(["ping", "-c 4", url])
    if output == 0:
        print("IP is reachable")
    else:
        print("IP is not reachable")
    return output

def all_ports(url):
    with ThreadPoolExecutor(max_workers=80) as executor:
        futures = [executor.submit(get_url, url, port) for port in range(1, 65536)]
        for future in as_completed(futures):
            port, is_open = future.result()
            if is_open:
                print(f"Port {port} is open")
        
def udp_scan(url, port):
    scan = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        scan.sendto(b'hello', (url, port))
        print(f"UDP port {port} is open")
    except Exception as e:
        print(f"UDP port {port} is closed")
    finally:
        scan.close()

def is_host_alive(ip_str, timeout=1):
    try:
        socket.getaddrinfo(ip_str, None)
        return True
    except Exception as e:
        return False

def scan_ports(url, start_port, end_port):
    with ThreadPoolExecutor(max_workers=70) as executor:
        futures = [executor.submit(get_url, url, port) for port in range(start_port, end_port)]
        for future in as_completed(futures):
            port, is_open = future.result()
            if is_open:
                print(f"Port {port} is open")

def main():
    try:
        args = get_arguments()
        start_time = time.time()

        if args.network:
            net = ipaddress.ip_network(args.network, strict=False)
            for ip in net.hosts():
                ip_str = str(ip)
                print(f"Checking host: {ip_str}")
                if is_host_alive(ip_str):
                    print(f"{ip_str} is alive")
                else:
                    print(f"{ip_str} is dead")

        elif args.udp_port:
            udp_scan(args.url, args.udp_port)
            return

        elif args.ping:
            ping_scan(args.url)
            return

        elif not args.url:
            print("Please specify the IP or hostname")
            return

        elif args.open:
            scan_ports(args.url, 1, 65535)

        elif args.ports:
            all_ports(args.url)

        elif args.port is not None:
            port, is_open = get_url(args.url, args.port)
            if is_open:
                print(f"Port {port} is open")
            else:
                print(f"Port {port} is closed")

        else:
            print("Please specify either a single port or use the -p- option to scan all ports.")

        end_time = time.time()
        print(f"Total time taken for all scans: {end_time - start_time} seconds")
    except KeyboardInterrupt:
        print("\n Exiting....")
if __name__ == "__main__":
    main()
