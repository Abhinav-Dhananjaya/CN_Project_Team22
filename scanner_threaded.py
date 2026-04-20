import socket
import ssl
import threading
import time

# --- CONFIGURATION ---
TARGET_IP = "127.0.0.1"        # Your friend scans their OWN machine
LOG_SERVER_IP = "10.43.137.98" # YOUR (server) WiFi IP — update this!
LOG_SERVER_PORT = 8443
THREADS_COUNT = 40
CERT_FILE = "cert.pem"         # cert.pem copied from server machine
# ---------------------

def report_to_server(message):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(CERT_FILE)
    context.check_hostname = False

    try:
        with socket.create_connection((LOG_SERVER_IP, LOG_SERVER_PORT), timeout=3) as sock:
            with context.wrap_socket(sock) as ssock:
                ssock.sendall(message.encode())
    except Exception as e:
        print(f"[!] Reporting failed: {e}")

def scan_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.0)
    result = s.connect_ex((TARGET_IP, port))
    if result == 0:
        try:
            s.settimeout(0.5)
            banner = s.recv(1024).decode(errors='ignore').strip()
            msg = f"Port {port} OPEN | Banner: {banner if banner else 'No banner'}"
        except:
            msg = f"Port {port} OPEN"
        print(f"[+] {msg}")
        report_to_server(msg)
    s.close()

def worker(port_list):
    for port in port_list:
        scan_port(port)

def run_distributed_scanner(start_port, end_port):
    ports = list(range(start_port, end_port + 1))
    threads = []
    chunk_size = max(1, len(ports) // THREADS_COUNT)

    print(f"[*] Scanning {TARGET_IP} ports {start_port}-{end_port} with {THREADS_COUNT} threads...")
    start_time = time.time()

    for i in range(0, len(ports), chunk_size):
        port_chunk = ports[i : i + chunk_size]
        t = threading.Thread(target=worker, args=(port_chunk,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"\n[*] Scan complete in {time.time() - start_time:.2f} seconds.")

if __name__ == "__main__":
    run_distributed_scanner(1, 1024)
