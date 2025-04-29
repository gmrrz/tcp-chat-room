import socket
import threading
from cryptography.fernet import Fernet

HOST = 'ezloomdev.cc'  # Change this to your server's IP or domain later
PORT = 12345

with open("key.key", "rb") as key_file:
    KEY = key_file.read()

f = Fernet(KEY)

def receive_messages(sock):
    while True:
        try:
            encrypted_msg = sock.recv(1024)
            if not encrypted_msg:
                break
            print(">>", f.decrypt(encrypted_msg).decode())
        except:
            break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Prompt for username
username = input("Enter your username: ").strip()
while not username:
    username = input("Username cannot be empty. Enter your username: ").strip()

# Send the username to the server
client.send(f.encrypt(username.encode()))

# Display chat history
try:
    encrypted_history = client.recv(1024)
    chat_history = f.decrypt(encrypted_history).decode()
    print("\n--- Chat History ---")
    print(chat_history)
    print("---------------------\n")
except:
    print("[!] Failed to load chat history.")

threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

print("Connected! Type your messages below:\n")

try:
    while True:
        msg = input()
        if msg.strip() == "":
            continue

        # If user types '/exit', send a goodbye message and exit
        if msg.lower() == "/exit":
            print("Exiting the chat...")
            client.send(f.encrypt(f"{username} has left the chat.".encode()))  # Notify server
            break
        
        # Prepend username to the message
        encrypted = f.encrypt(f"{username}: {msg}".encode())
        client.send(encrypted)

except KeyboardInterrupt:
    print("\n[!] You have left the chat.")
    client.send(f.encrypt(f"{username} has left the chat.".encode()))  # Notify server

finally:
    client.close()
    print("[!] Connection closed.")