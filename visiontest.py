import socket
import os
import dotenv
import json
dotenv.load_dotenv()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((socket.gethostname(), int(os.getenv("VISION_PORT"))))

while True:
    data = client_socket.recv(1024).decode('utf-8')
    data = json.loads(data)
    
    if data['exit_signal'] :
        break
    else:
        print(data)