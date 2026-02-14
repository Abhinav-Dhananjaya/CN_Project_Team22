import socket
import ssl

def report_to_server(message):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    with socket.create_connection(("127.0.0.1", 8443)) as sock:
        with context.wrap_socket(sock, server_hostname="127.0.0.1") as ssock:
            ssock.sendall(message.encode())

def scan_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.5)
    result = s.connect_ex((ip, port))
    if result == 0:
        msg = f"Port {port} is OPEN"
        try:
            banner = s.recv(1024).decode().strip()
            msg += f" | Service: {banner}"
        except:
            msg += " | Service: Unknown"
        print(msg)
        report_to_server(msg)
    s.close()

if __name__ == "__main__":
    target = "127.0.0.1"
    for p in [22, 80, 443, 8443]:
        scan_port(target, p)
