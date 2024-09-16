import socket
import argparse
import subprocess
import ipaddress
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_arguments():
    parser = argparse.ArgumentParser(
        description=(
            "NOTE: If you want to scan all ports, optimize according to your system specs:\n"
            " - 4GB RAM: Workers (--workers): 4-8 threads, Batch Size (--batch-size): 200 - 500\n"
            " - 6GB RAM: Workers (--workers): 8-16 threads, Batch Size (--batch-size): 500 - 1000 \n"
            " - 8GB RAM: Workers (--workers): 16-32 threads, Batch Size (--batch-size): 1000 - 2000 \n"
            " - 16GB RAM: Workers (--workers): 32-64 threads, Batch Size (--batch-size): 2000-4000"
        )
    )
    parser.add_argument("-u", "--url", dest="url", help="use URL or IP of the domain to scan")
    parser.add_argument("-sn", "--ping", action="store_true", help="ping the target")
    parser.add_argument("-o", "--open", action="store_true", help="show only open ports")
    parser.add_argument("-sU", "--udp", dest="udp_port", type=int, nargs='?', const=None, help="scan UDP ports")
    parser.add_argument("-p", "--port", type=int, dest="port", help="scan a specific port")
    parser.add_argument("-n", "--network", dest="network", help="check alive hosts in the network")
    parser.add_argument("-p-", "--ports", action="store_true", help="scan all ports")
    parser.add_argument("-w", "--workers", type=int, default=150, help="number of concurrent workers")
    parser.add_argument("-b", "--batch-size", type=int, default=10000, help="size of each batch for port scanning")
    return parser.parse_args()

def get_url(url, port):
    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scanner.settimeout(1)
    try:
        conn = scanner.connect_ex((url, port))
        if conn == 0:  # If port is open
            return port, True
        else:
            return port, False
    except Exception as e:
        print(f"Error scanning port {port}: {e}")
        return port, False
    finally:
        scanner.close()

def all_ports(url, batch_size, max_workers):
    total_ports = 65535
    batches = [(start, min(start + batch_size - 1, total_ports)) for start in range(1, total_ports + 1, batch_size)]

    for batch_num, (start_port, end_port) in enumerate(batches, 1):
        print(f"\nScanning batch {batch_num}: Ports {start_port} - {end_port}")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(get_url, url, port) for port in range(start_port, end_port + 1)]
            try:
                for future in as_completed(futures):
                    port, is_open = future.result()
                    if is_open:
                        print(f"Port {port} is open")  # Print only if port is open
            except KeyboardInterrupt:
                print("\nScan interrupted. Cleaning up...")
                executor.shutdown(wait=False)  # Attempt to stop the executor

def scan_ports(url, start_port, end_port, max_workers):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(get_url, url, port) for port in range(start_port, end_port)]
        try:
            for future in as_completed(futures):
                port, is_open = future.result()
                if is_open:
                    print(f"Port {port} is open")
        except KeyboardInterrupt:
            print("\nScan interrupted. Cleaning up...")
            executor.shutdown(wait=False)  # Attempt to stop the executor


def ping_scan(url):
    output = subprocess.call(["ping", "-c 4", url])
    if output == 0:
        print("IP is reachable")
    else:
        print("IP is not reachable")
    return output

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

def scan_ports(url, start_port, end_port, max_workers):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
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
            scan_ports(args.url, 1, 1024, args.workers)

        elif args.ports:
            all_ports(args.url, batch_size=args.batch_size, max_workers=args.workers)

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
