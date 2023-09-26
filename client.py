import socket
import threading

# Create a socket client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8080))  

# User input for user_id and group_id
user_id = input("Enter your user_id: ")
group_id = input("Enter the group_id you want to join: ")

# Send user_id and group_id to the server
message = str(user_id)+':'+str(group_id)
client.send(message.encode('utf-8'))


# Function to send messages
def send_message():
    while True:
        message = input('Send message (send END to end conversation) : ')
        if message=="END":
            print("Bye!")
            client.close()
            return
        client.send(message.encode('utf-8'))

# Create a thread for sending messages
send_thread = threading.Thread(target=send_message)
send_thread.start()

# Receive and print messages from the server
while True:
    details = client.recv(1024).decode('utf-8')
    sender, text=details.split(':')
    print(' ')
    print(sender+": "+text)
    print('Send message (send END to end conversation) in the next line ')



