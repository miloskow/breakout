import speech_recognition as sr
import time
import threading
import pygame

pygame.init()
WIDTH = 350
HEIGHT = 150
screen = pygame.display.set_mode((WIDTH, HEIGHT))
running = True

def recognize_voice_command(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for a command...")
        audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
        try:
            command = recognizer.recognize_google(audio)
            print("You said: " + command)
            return command.lower()
        except sr.UnknownValueError:
            print("Audio couldnt be understood.")
            return None

def handle_voice_commands(recognizer, microphone):
    global running
    while running:
        try:
            command = recognize_voice_command(recognizer, microphone)
            if command:
                if "quit" in command:
                    running = False
                elif "hello" in command:
                    print("Hello there!")
                    
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for a phrase to start")
        except sr.RequestError as e:
            print(f"Could not request results, {e}")

        time.sleep(0.1)

recognizer = sr.Recognizer()
microphone = sr.Microphone()

voice_thread = threading.Thread(target=handle_voice_commands, args=(recognizer,microphone))
voice_thread.start()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
voice_thread.join()