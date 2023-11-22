import socket
import threading

def authenticate_user(client_socket):
    # Receive and print the authentication prompts from the server
    prompt_username = client_socket.recv(1024).decode('utf-8')
    print(prompt_username, end="")
    
    # Send the username to the server
    username = input()
    client_socket.sendall(username.encode('utf-8'))

    # Receive and print the password prompt from the server
    prompt_password = client_socket.recv(1024).decode('utf-8')
    print(prompt_password, end="")

    # Send the password to the server
    password = input()
    client_socket.sendall(password.encode('utf-8'))

   
    return username

def file_transfer(client):
    #Opening and reading the file data.
    file = open("data/text.txt","r")
    data = file.read()
    #sending the filename to the server
    client.sendall("text.txt".encode('utf-8'))
    msg = client.recv(1024).decode('utf-8')
    print(f"[SERVER]: {msg}")
    #sending the file data to the server
    client.sendall(data.encode('utf-8'))
    msg = client.recv(1024).decode('utf-8')
    print(f"[SERVER]: {msg}")
    #closing the file 
    file.close()

def chat(client):
    while True:
        try:

            message = input("Enter your message: ")
            client.sendall(message.encode('utf-8'))

            data = client.recv(1024).decode('utf-8')
            print(f"Received from server: {data}")

        except Exception as e:
            print(f"Error communicating with the server: {e}")
            break

    print("Connection closed.")

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.2', 9999))

    # Perform user authentication
    authenticated_user = authenticate_user(client)

    if not authenticated_user:
        print("Authentication failed. Exiting.")
        client.close()
        return

    print(f"Authenticated as {authenticated_user}. Connection established.")
    # Apply file transfer
    file_transfer(client)
    
    chat(client)
    client.close()

if __name__ == "__main__":
    main()



