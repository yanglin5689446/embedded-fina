
from google_speech import Speech
import speech_recognition as sr
from food_stalls import food_stalls
from line import line_send_to
import editdistance

class Assistant:
    def __init__(self, lang="zh-TW"):
        self.lang = lang
        self.food_stall = ''
        self.init_google_recognizer() 
    def init_google_recognizer(self):
        with sr.Microphone(device_index=2) as source:
            self.recognizer = sr.Recognizer()
            self.recognizer.adjust_for_ambient_noise(source, duration=3)
    def listen_speech(self, timeout=3, phrase_time_limit=5):
        with sr.Microphone(device_index=2) as source:
            self.audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
    def recognize_audio(self):
        try:
            return self.recognizer.recognize_google(self.audio, language=self.lang)
        except sr.UnknownValueError:
            return None
        except sr.RequestError as err:
            print("No response from Google Speech Recognition service: {0}".format(err))
    def listen_and_recognize(self):
        self.listen_speech()
        return self.recognize_audio()
    def speak(self, message):
        speech = Speech(message, self.lang)
        speech.play(("speed", "1"))
        print(message)
    def search_food_stall(self, query):
        best_distance = 1e9
        best_match = None
        for name, food_stall in food_stalls.items():
            for keyword in food_stall['keywords']:
                distance = editdistance.eval(query, keyword) / len(query)
                if distance < best_distance:
                    best_match = name 
                    best_distance = distance
        return (best_match, best_distance)
    def search_menu(self, query):
        best_distance = 1e9
        best_match = None
        for item in food_stalls[self.food_stall]['menu'].keys():
            distance = editdistance.eval(query, item) / len(query)
            if distance < best_distance:
                best_match = item 
                best_distance = distance
        return (best_match, best_distance)
    def confirm(self):
        positive_replies = ('是', '是的', '對', '對的', '正確', '沒錯', 'OK')     
        user_reply = self.listen_and_recognize()
        return self._semantic_analysis(user_reply, positive_replies) < 0.5
    def send_orders(self, orders):
        message = self._assemble_message(orders)
        print(message)
        line_send_to(message=message)
        
    def _semantic_analysis(self, query, phrases):
        best_distance = 1e9
        if not query:
            return 1e9
        for phrase in phrases:
            best_distance = min(best_distance, editdistance.eval(query, phrase) / len(query))
        return best_distance

    def _assemble_message(self, orders):
        first = True
        message = ""
        for item, amount in orders.items():
            if not first :
                message += ","
            first = False
            message += "{0} {1}份".format(item, amount)
        return message

