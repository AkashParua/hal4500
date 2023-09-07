import socket
import os
from dotenv import load_dotenv
load_dotenv()

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect((socket.gethostname(), int(os.getenv("HEARING_PORT"))))
while True:
    data = soc.recv(1024).decode('utf-8')
    if data:
        print(data)
        if data == "exit":
            break
soc.close()