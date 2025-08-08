#!/usr/bin/python3
import socket
import threading
import sys
sys.argv

# CONFIGURATION
TO_HOST = '127.0.0.1' 
LOCAL_HOST = '0.0.0.0'     

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 tunnla.py <target_port> <new_port_to_open>")
        sys.exit(1)
    try:
        global TO_PORT; global FROM_PORT
        TO_PORT = int(sys.argv[1])
        FROM_PORT = int(sys.argv[2])
    except ValueError:
        print('Only numbers are allow.')
        return

    start_tunnel(FROM_PORT, TO_PORT)


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

        # Start forwarding in both directions
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
    main()
    print('Exiting.')
