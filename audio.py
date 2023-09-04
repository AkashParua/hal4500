import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()

while True:
    with sr.Microphone() as source:
        print("Listening... Speak something:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    print("Recognition complete. Transcribing...")

    try:
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
        
        if "Alex" in text:
            print("Alex is summoned!")

    except sr.UnknownValueError:
        print("Google Web Speech API could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API; {e}")
