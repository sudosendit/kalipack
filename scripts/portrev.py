import socket
import threading

# CONFIGURATION
TO_HOST = '127.0.0.1'      
TO_PORT = 19999           # Duplicating

LOCAL_HOST = '0.0.0.0'     
FROM_PORT = 4321         # Reporting from

def forward(source, destination):
    try:
        while True:
            data = source.recv(4096)
            if not data:
                break
            destination.sendall(data)
    finally:
        source.close()
        destination.close()

def handle_client(client_socket):
    try:
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((TO_HOST, TO_PORT))

        # fwd in both directions
        threading.Thread(target=forward, args=(client_socket, remote_socket)).start()
        threading.Thread(target=forward, args=(remote_socket, client_socket)).start()
    except Exception as e:
        print(f"[!] Error: {e}")
        client_socket.close()

def start_tunnel():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((LOCAL_HOST, FROM_PORT))
    server.listen(5)
    print(f"[+] Tunnel running: forwarding port {FROM_PORT} → {TO_HOST}:{TO_PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"[+] Connection from {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == '__main__':
    start_tunnel()
