import socket
import time

TARGET_IP = "127.0.0.1"

def scan_ports(start_port, end_port):
    print(f"[*] Starting basic scan on {TARGET_IP}...")
    print(f"[*] Scanning ports {start_port} to {end_port}...\n")
    start_time = time.time()
    open_ports = []

    for port in range(start_port, end_port + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)

        result = s.connect_ex((TARGET_IP, port))
        if result == 0:
            # Try to grab banner/service name
            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown"
            print(f"[+] Port {port} OPEN | Service: {service}")
            open_ports.append(port)
        s.close()

    end_time = time.time()
    print(f"\n[*] Scan complete in {end_time - start_time:.2f} seconds.")
    print(f"[*] Total open ports found: {len(open_ports)}")
    if open_ports:
        print(f"[*] Open ports: {open_ports}")

if __name__ == "__main__":
    scan_ports(1, 1024)
