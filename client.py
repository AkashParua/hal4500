import socket
import json
import os
import dotenv
dotenv.load_dotenv()

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1',int(os.getenv("VISION_PORT")))

client_socket.connect(server_address)

vision_data = None

while True :
    
    data = client_socket.recv(1024).decode('utf-8')
    if data :
        recv_data = json.loads(data)
        print(recv_data['exit_signal'])
        if recv_data['exit_signal'] :
            break


    







    