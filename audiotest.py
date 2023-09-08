import socket
import os
from dotenv import load_dotenv
load_dotenv()


soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.setblocking(False)

soc.connect((socket.gethostname(), int(os.getenv("HEARING_PORT"))))
while True:
    data = None
    try :
        data = soc.recv(1024).decode('utf-8')
    except BlockingIOError:
        pass

    if data:
        if data == "exit":
            break
    
        print(data)


soc.close()