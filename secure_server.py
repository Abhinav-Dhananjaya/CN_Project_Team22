import socket
import ssl

def run_secure_server():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    bind_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bind_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    bind_sock.bind(('0.0.0.0', 8443))
    bind_sock.listen(5)

    print("[*] SSL Server listening on port 8443")
    print("[*] Share YOUR IP with your friend so they can connect")
    print("[*] Run 'ipconfig' to find your WiFi IPv4 address")

    while True:
        newsocket, fromaddr = bind_sock.accept()
        try:
            with context.wrap_socket(newsocket, server_side=True) as secure_conn:
                data = secure_conn.recv(1024).decode()
                if data:
                    print(f"\n[SECURE REPORT] From {fromaddr[0]}: {data}")
        except ssl.SSLError as e:
            print(f"[!] SSL Handshake failed: {e}")
        except Exception as e:
            print(f"[!] Error: {e}")
        finally:
            newsocket.close()

if __name__ == "__main__":
    run_secure_server()
