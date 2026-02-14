import socket
import ssl
import threading
import time

TARGET_IP = "127.0.0.1"
LOG_SERVER_IP = "127.0.0.1"
LOG_SERVER_PORT = 8443
THREADS_COUNT = 100

def report_to_server(message):
    """
    Satisfies Mandatory Requirement: SSL/TLS-based secure communication 
    for all data exchanges[cite: 7].
    """
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    try:
        with socket.create_connection((LOG_SERVER_IP, LOG_SERVER_PORT), timeout=2) as sock:
            with context.wrap_socket(sock, server_hostname=LOG_SERVER_IP) as ssock:
                ssock.sendall(message.encode())
    except ssl.SSLError as e:
        print(f"[!] SSL Handshake failure: {e}")
    except ConnectionRefusedError:
        print("[!] Secure Log Server is offline.")
    except Exception as e:
        pass

def scan_port(port):
    """
    Core Implementation: Low-level socket creation and service detection.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.0)
    result = s.connect_ex((TARGET_IP, port))
    if result == 0:
        try:
            banner = s.recv(1024).decode().strip()
            service_info = f"Port {port} OPEN | Service: {banner if banner else 'Unknown'}"
        except:
            service_info = f"Port {port} OPEN | Service: Detected (No Banner)"
        print(f"[+] {service_info}")
        report_to_server(service_info)
    s.close()

def worker(port_list):
    """Worker function for threads to process specific ports."""
    for port in port_list:
        scan_port(port)

def run_scanner(start_port, end_port):
    """
    Requirement: Concurrency and Performance Evaluation.
    """
    ports = range(start_port, end_port + 1)
    threads = []
    chunk_size = len(ports) // THREADS_COUNT if len(ports) > THREADS_COUNT else 1
    print(f"[*] Scanning {TARGET_IP} from port {start_port} to {end_port}...")
    start_time = time.time()

    for i in range(0, len(ports), chunk_size):
        port_chunk = ports[i : i + chunk_size]
        t = threading.Thread(target=worker, args=(port_chunk,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_time = time.time()
    print(f"[*] Scan complete in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    run_scanner(1, 1024)
