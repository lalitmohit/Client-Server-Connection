import socket
import threading

# Dictionary to store user credentials (username: password)
user_credentials = {
    'lalitg': 'Lalit1306@',
    'sahil': '12140080',
    # Add more users as needed
}

def authenticate_user(client_socket):
    # Ask the client for a username and password
    client_socket.sendall("Enter your username: ".encode('utf-8'))
    username = client_socket.recv(1024).decode('utf-8')

    client_socket.sendall("Enter your password: ".encode('utf-8'))
    password = client_socket.recv(1024).decode('utf-8')

    # Check if the provided username and password are valid
    if username in user_credentials and user_credentials[username] == password:
        return username
    else:
        return None

def file_transfer(client_socket):
    #Receiving the filename
    filename = client_socket.recv(1024).decode('utf-8')
    file = open(filename,"w")
    client_socket.sendall("Filename Received: ".encode('utf-8'))
    file_data = client_socket.recv(1024).decode('utf-8')
    file.write(file_data)
    client_socket.sendall("Filedata received: ".encode('utf-8'))
    file.close()

def chat(client_socket):
    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(1024).decode('utf-8')

            if not data:
                break

            print(f"Received from client: {data}")
        
            # Echo the received message back to the client
            client_socket.sendall(data.encode('utf-8'))
            # data=False

        except Exception as e:
            print(f"Error handling client: {e}")
            break

def handle_client(client_socket):
    # Perform user authentication
    authenticated_user = authenticate_user(client_socket)

    if not authenticated_user:
        print("Authentication failed. Closing connection.")
        client_socket.close()
        return

    print(f"User {authenticated_user} authenticated. Connection established.")

    # Continue with the rest of the client communication logic...
    # ...
    file_transfer(client_socket)
    chat(client_socket)

    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)

    print("[*] Listening on 0.0.0.0:9999")

    while True:
        client, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == "__main__":
    main()
