import socket
import threading

# Dictionary to store connected users and their groups
users = {}

# Function to handle client connections
def handle_client(client_socket, user_id, group_id):
    try:
        # Add the user to the group
        if group_id in users:
            users[group_id].append((user_id, client_socket))
        else:
            users[group_id] = [(user_id, client_socket)]
        
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            print("User "+user_id+" from "+group_id+" sent "+message)
            if not message or message=="END":
                print("Connection closed.")
                break
            # Broadcast the message to all users in the group
            for _, user_socket in users[group_id]:
                if user_socket != client_socket:
                    details = str(user_id) + ':' + message
                    user_socket.send(details.encode('utf-8'))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        users[group_id].remove((user_id, client_socket))
        client_socket.close()

# Create a socket server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 8080))
server.listen(5)

print("Server listening on port 8080")

while True:
    client_sock, addr = server.accept()
    message = client_sock.recv(1024).decode('utf-8')
    user_id, group_id = message.split(':')
    print(f"Received connection from "+user_id+" in group "+group_id)
    
    # Create a new thread to handle the client
    client_handler = threading.Thread(target=handle_client, args=(client_sock, user_id, group_id))
    client_handler.start()
