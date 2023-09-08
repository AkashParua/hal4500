import socket
import json
import os
import dotenv
dotenv.load_dotenv()

vision_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostname(), int(os.getenv("MAIN_PORT"))))
server_socket.listen(1)
print("main server is listening...")

vision_socket.connect((socket.gethostname(), int(os.getenv("VISION_PORT"))))
audio_socket.connect((socket.gethostname(), int(os.getenv("HEARING_PORT"))))

audio_socket.settimeout(0)



client_socket, client_address = server_socket.accept()


def perception():
   
    while True:
        visual_data = None
        audio_data = None
        visual_input = vision_socket.recv(1024).decode('utf-8')
        try:
            audio_input = audio_socket.recv(1024).decode('utf-8')
        except socket.timeout:
            audio_input = None


        if visual_input:
            visual_data = json.loads(visual_input)

        if audio_input and audio_input != "--silence--":
            audio_data = audio_input
        
        if visual_data['exit_signal'] :
            audio_socket.send("exit".encode('utf-8'))
            break
      
        
        response = {
            "audio": audio_data,
            "visual": visual_data
        }


        json_response = json.dumps(response)
        client_socket.send(json_response.encode('utf-8'))

    
    client_socket.close()
    audio_socket.close()
    vision_socket.close()


perception()
        
'''
{
    audio : String
    visual : {
            'left_hand_object' : {
                'name' : float,
                'xmin' : float,
                'ymin' : float,
                'xmax' : float,
                'ymax' : None
            },
            'right_hand_object' : {
                'name' : None,
                'xmin' : None,
                'ymin' : None,
                'xmax' : None,
                'ymax' : None
            }, 
            'right_hand_poisture' : String,
            'left_hand_poisture' : String,
            'exit_signal' : boolean
        }
}
'''
        


        

          








'''
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
'''

    







    