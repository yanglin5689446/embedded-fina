
import speech_recognition as sr

class Recognizer:
    def __init__(self):
        self.init_google_recognizer()
    def init_google_recognizer(self):
        with sr.Microphone() as source:
            self.recognizer = sr.Recognizer()
            self.recognizer.adjust_for_ambient_noise(source, duration=3)
    def listen_speech(self):
        with sr.Microphone() as source:
            self.audio = self.recognizer.listen(source)
    def recognize_audio(self):
        try:
            return self.recognizer.recognize_google(self.audio, language="zh-TW")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as err:
            print("No response from Google Speech Recognition service: {0}".format(err))

