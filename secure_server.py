import socket
import ssl

def start_secure_server():
    bind_ip = "127.0.0.1"
    bind_port = 8443
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    print(f"[*] Secure Server listening on {bind_ip}:{bind_port}")
    while True:
        client_sock, address = server.accept()
        secure_conn = context.wrap_socket(client_sock, server_side=True)
        print(f"[*] Secure connection established with {address}")

        data = secure_conn.recv(1024)
        if data:
            print(f"[*] Received Secure Report: {data.decode()}")

        secure_conn.close()

if __name__ == "__main__":
    start_secure_server()
