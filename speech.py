import speech_recognition as sr
import time


class SpeechRec:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.working = True
        

        try:
            self.microphone = sr.Microphone()
        except OSError:
            print("No microphone detected. Voice commands disabled.")
            self.working = False
            self.microphone = None

    def recognize_voice_command(self):
        if not self.microphone:
            return None

        with self.microphone as source:
            print("Kalibracja mikrofonu...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

            print("Nasłuchiwanie...")
            try:
                audio = self.recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=3
                )
            except sr.WaitTimeoutError:
                print("Timeout — nic nie powiedziano.")
                return None

        try:
            command = self.recognizer.recognize_google(
                audio,
            )

            command = command.lower()
            print("Powiedziałeś:", command)
            return command

        except sr.UnknownValueError:
            print("Nie rozpoznano mowy.")
            return None

        except sr.RequestError as e:
            print(f"Błąd API: {e}")
            return None

    def handle_voice_commands(self):
        while self.working:
            command = self.recognize_voice_command()

            if command:
                if "stop" in command:
                    self.working = False
                    return "stop"

                return command

            time.sleep(0.1)

        return ""
