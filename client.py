import socket
import json
# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1',6000)

client_socket.connect(server_address)

vision_data = None

while True :
    
    data = client_socket.recv(1024).decode('utf-8')
    if data :
        recv_data = json.loads(data)
        print(recv_data)
        if recv_data['exit_signal'] :
            break










    