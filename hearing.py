import speech_recognition as sr
import socket
import os
from dotenv import load_dotenv
# Initialize the recognizer
load_dotenv()
recognizer = sr.Recognizer()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostname(), int(os.getenv("HEARING_PORT"))))
server.listen(1)
print("Server is listening...")

client_socket, address = server.accept()
print(f"Connection from {address} has been established!")

def listen():
    while True:
        audio_command = "--silence--"
        with sr.Microphone() as source:
            print("Listening... Speak something:")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        print("Recognition complete. Transcribing...")

        try:
            text = recognizer.recognize_google(audio)
            print("You said: " + text)
            audio_command = text
        except sr.UnknownValueError:
            print("Google Web Speech API could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")
        
        
        client_socket.send(audio_command.encode('utf-8'))
        
        if audio_command == "exit":
            break

    client_socket.close()
    server.close()

listen()

