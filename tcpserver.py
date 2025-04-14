import socket
import threading
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

#Server Configuration
HOST = "0.0.0.0"
PORT = 12345
clients = []

# Encryption key
ENCRYPTION_KEY = b"0123456789abcdef"  # 16 bytes key for AES-128

# Encrypt a message
def encrypt_message(message):
    iv = os.urandom(16)  # Initialization vector
    cipher = Cipher(algorithms.AES(ENCRYPTION_KEY), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_message = encryptor.update(message.encode()) + encryptor.finalize()
    return iv + encrypted_message  # Prepend IV to the encrypted message

def decrypt_message(encrypted_message):
    iv = encrypted_message[:16]  # Extract the IV from the beginning
    cipher = Cipher(algorithms.AES(ENCRYPTION_KEY), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(encrypted_message[16:]) + decryptor.finalize()
    return decrypted_message.decode()

# Broadcast a message to all clients
def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)

# Handle individual client connections
def handle_client(client_socket):
    while True:
        try:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                break
            message = decrypt_message(encrypted_message)
            print(f"Received: {message}")
            broadcast(encrypt_message(message), client_socket)
        except:
            clients.remove(client_socket)
            break

    client_socket.close()

    # Start the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server started on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()