import socket
import threading
import hashlib
import json
import re
from light_sim import SmartLight
from vigenere import VigenereCipher
# all neccesary lib/modules imported

def start_server():
    host = 'localhost'
    port = 12345

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Server listening on port", port)

    light = SmartLight()
    cipher = VigenereCipher("YOURKEY")

    while True:
        conn, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, address, light, cipher))
        client_thread.start()


def send_register_command(client_socket, cipher, username, password):
    command = f"REGISTER {username} {password}"
    encrypted_message = cipher.encrypt(command)
    client_socket.send(encrypted_message.encode())
    data = client_socket.recv(1024).decode()
    decrypted_data = cipher.decrypt(data)
    
    if decrypted_data == "Registration successful":
        return True, None  # Success, no password strength details needed
    else:
        password_strength = json.loads(decrypted_data)
        return False, password_strength  # Registration failed, return password strength details
    


def create_user(username, password): #creates a user/ register
    hashed_password = hashlib.sha256(password.encode()).hexdigest() #password is hashed for security
    try:
        with open('users.json', 'r+') as file:
            try:
                users = json.load(file)
            except json.JSONDecodeError:
                users = {}  # initialize as an empty dictionary if file is empty/ Error was thrown if j.son file was empty
            if username in users: # checks for existing enteries of users
                return False 
            users[username] = hashed_password 
            file.seek(0)
            json.dump(users, file)
    except FileNotFoundError: # adds new use users.json file if it doesnt exist
        with open('users.json', 'w') as file:
            users = {username: hashed_password}
            json.dump(users, file)
    return True

def login_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest() #hexidigest() converts to hexidecimal string
    with open('users.json', 'r') as file:
        users = json.load(file)
        if username in users and users[username] == hashed_password: #checks if user and password is corrrect 
            return True  # Login successful
    return False

def handle_client(conn, address, light, cipher): #handles all the commands and client data
    print(f"Connection from: {address} Connected.") 
    user_logged_in = False #tracks if user is logged in

    while True:
        encrypted_data = conn.recv(1024).decode() #recieves data limited to 1024 bytes
        if not encrypted_data: 
            break

        decrypted_data = cipher.decrypt(encrypted_data) #decrypts the data using cipher
        print(f"Encrypted message from {address}: {encrypted_data}") #printing ONLY the encrypted data for security 
        #print(f"Decrypted message fomr {address: {decrypted_data}}") this could also be added but its not safe

        if decrypted_data.startswith("REGISTER"): 
            _, username, password = decrypted_data.split() # only interested in username and password 
            success = create_user(username, password) 
            response = "Registration successful" if success else "Registration failed"
        elif decrypted_data.startswith("LOGIN"):
            _, username, password = decrypted_data.split()
            user_logged_in = login_user(username, password)
            response = "Login successful" if user_logged_in else "Login failed"
        elif user_logged_in:
            #process light control commands
            if decrypted_data == "ON":
                light.set_state("ON")
                response = "Light is now ON"
            elif decrypted_data == "OFF":
                light.set_state("OFF")
                response = "Light is now OFF"
            elif decrypted_data.startswith("BRIGHTNESS"):
                try:
                    _, level = decrypted_data.split()
                    brightness_level = int(level)
                    if 0 <= brightness_level <= 100:
                        light.set_brightness(brightness_level)
                        response = f"Brightness set to {brightness_level}"
                    else:
                        response = "Brightness level must be between 0 and 100"
                except ValueError:
                    response = "Invalid brightness command"
            else:
                response = "Unknown command"
        else:
            response = "Please login or register"

        encrypted_response = cipher.encrypt(response)
        conn.send(encrypted_response.encode())

    conn.close()
    print(f"Connection with {address} closed.")



if __name__ == '__main__':
    start_server()
