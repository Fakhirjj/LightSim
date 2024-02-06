import socket
from vigenere import VigenereCipher

def send_command(client_socket, cipher, command):
    encrypted_message = cipher.encrypt(command)
    client_socket.send(encrypted_message.encode())
    data = client_socket.recv(1024).decode()
    decrypted_data = cipher.decrypt(data)
    print("Server response: " + decrypted_data)

def start_client():
    host = 'localhost'
    port = 12345

    client_socket = socket.socket()
    client_socket.connect((host, port))

    cipher = VigenereCipher("YOURKEY")

    while True:
        action = input("Choose action (REGISTER, LOGIN, COMMAND, QUIT): ")
        if action == "QUIT":
            break
        elif action == "REGISTER":
            username = input("Enter username: ")
            password = input("Enter password: ")
            send_command(client_socket, cipher, f"REGISTER {username} {password}")
        elif action == "LOGIN":
            username = input("Enter username: ")
            password = input("Enter password: ")
            send_command(client_socket, cipher, f"LOGIN {username} {password}")
        elif action == "COMMAND":
            command = input("Enter command (ON, OFF, BRIGHTNESS [0-100]): ")
            send_command(client_socket, cipher, command)

    client_socket.close()

if __name__ == '__main__':
    start_client()
