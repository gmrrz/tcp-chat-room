import socket
import time
import threading
from cryptography.fernet import Fernet

HOST = '0.0.0.0'
PORT = 12345

with open("key.key", "rb") as key_file:
    KEY = key_file.read()

f = Fernet(KEY)
clients = []

def broadcast(msg, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.send(msg)
            except:
                clients.remove(client)
                client.close()

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    clients.append(conn)
    while True:
        try:
            encrypted_msg = conn.recv(1024)
            if not encrypted_msg:
                break
            decrypted_msg = f.decrypt(encrypted_msg).decode()
            print(f"[{addr}] {decrypted_msg}")
        
            broadcast(encrypted_msg, conn)
        except:
            break
    print(f"[DISCONNECTED] {addr} disconnected.")
    clients.remove(conn)
    conn.close()

def start_server():
    # TCP connection
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket.SOCK_STREAM is TCP conncetion
    server.bind((HOST, PORT))
    server.listen()
    server.settimeout(1.0)
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")
    try:
        while True:
            try:
                conn, addr = server.accept()
                thread = threading.Thread(target=handle_client, args=(conn, addr))
                thread.daemon = True  # Threads won't block shutdown
                thread.start()
            except socket.timeout:
                continue  # just retry after timeout
    except KeyboardInterrupt:
        print("\n[!] KeyboardInterrupt detected. Shutting down server.")
        server.close()
        time.sleep(1)  # give threads a moment to close if needed
        exit(0)


start_server()

