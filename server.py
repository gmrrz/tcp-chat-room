import socket
import time
import threading
from cryptography.fernet import Fernet

HOST = '0.0.0.0'
PORT = 12345

with open("key.key", "rb") as key_file:
    KEY = key_file.read()

f = Fernet(KEY)
clients = {}

def broadcast(msg, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.send(msg)
            except:
                del clients[client]
                client.close()

def handle_client(conn, addr):
    print(f"[+] New connection from {addr}")
    
    # Receive and store the username
    try:
        encrypted_username = conn.recv(1024)
        username = f.decrypt(encrypted_username).decode()
    except:
        print(f"[-] Failed to retrieve username from {addr}. Disconnecting.")
        conn.close()
        return

    clients[conn] = username
    print(f"[+] {username} ({addr}) has joined the chat.")
    broadcast(f.encrypt(f"{username} has joined the chat.".encode()), conn)

    # Send chat history to the new client
    try:
        with open("chat_log.txt", "r") as log:
            history = log.read()
        if not history.strip():
            history = "No chat history available."
        conn.send(f.encrypt(history.encode()))
    except FileNotFoundError:
        conn.send(f.encrypt("No chat history available.".encode()))
    except Exception as e:
        print(f"[!] Error sending chat history to {username}: {e}")
        conn.send(f.encrypt("Failed to load chat history.".encode()))

    while True:
        try:
            encrypted_msg = conn.recv(1024)
            if not encrypted_msg:
                break
            decrypted_msg = f.decrypt(encrypted_msg).decode()
            print(decrypted_msg)  # Log the message as-is (already includes username)

            # Log the message
            with open("chat_log.txt", "a") as log:
                log.write(f"{decrypted_msg}\n")

            broadcast(encrypted_msg, conn)  # Broadcast the message as-is
        except:
            break

    print(f"[-] {username} ({addr}) disconnected.")
    broadcast(f.encrypt(f"{username} has left the chat.".encode()), conn)
    del clients[conn]
    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    server.settimeout(1.0)
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")
    try:
        while True:
            try:
                conn, addr = server.accept()
                thread = threading.Thread(target=handle_client, args=(conn, addr))
                thread.daemon = True
                thread.start()
            except socket.timeout:
                continue
    except KeyboardInterrupt:
        print("\n[!] KeyboardInterrupt detected. Shutting down server.")
        server.close()
        time.sleep(1)
        exit(0)

start_server()