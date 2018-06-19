
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
        with sr.Microphone(sample_rate=44100) as source:
            self.recognizer = sr.Recognizer()
            self.recognizer.adjust_for_ambient_noise(source)
    def listen_speech(self, timeout=3, phrase_time_limit=5):
        with sr.Microphone(sample_rate=44100) as source:
            self.audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
    def recognize_audio(self):
        try:
            return self.recognizer.recognize_google(self.audio, language=self.lang)
        except sr.UnknownValueError:
            return None
        except sr.WaitTimeoutError:
            return None
        except sr.RequestError as err:
            print("No response from Google Speech Recognition service: {0}".format(err))

    def listen_and_recognize(self):
        self.listen_speech()
        return self.recognize_audio()
    def say(self, message):
        print(message)
        speech = Speech(message, self.lang)
        speech.play(("speed", "1.1"))
    def search_food_stall(self, query):
        best_distance = 1e9
        best_match = None
        for name, food_stall in food_stalls.items():
            for keyword in food_stall['keywords']:
                distance = editdistance.eval(query, keyword) / max(len(query), len(keyword))
                if distance < best_distance:
                    best_match = name 
                    best_distance = distance
        return (best_match, best_distance)
    def search_menu(self, query):
        best_distance = 1e9
        best_match = None
        for item in food_stalls[self.food_stall]['menu'].keys():
            distance = editdistance.eval(query, item) / max(len(query), len(item))
            if distance < best_distance:
                best_match = item 
                best_distance = distance
        return (best_match, best_distance)
    
    def check_cancel(self, message):
        possible_replies = ['取消']
        result = self._semantic_analysis(message, possible_replies)
        print(result)
        return result <= 0.5

    def confirm(self):
        positive_replies = ('是', '是的', '對', '對的', '正確', '沒錯', 'OK', '好')
        negative_replies = ('否', '不是', '錯', '不對', '錯誤', 'NO', '不要')

        user_reply = self.listen_and_recognize()
        negative = self._semantic_analysis(user_reply, negative_replies)
        positive = self._semantic_analysis(user_reply, positive_replies)

        return positive < negative

    def check_order_finish(self, query):
        replies = ('就這樣', '好了', '結束', '點完了')
        return self._semantic_analysis(query, replies) < 0.5

    def send_orders(self, orders):
        message = self._assemble_message(orders)
        line_send_to(message=message)
        
    def _semantic_analysis(self, query, phrases):
        best_distance = 1e9
        if not query:
            return 1e9
        for phrase in phrases:
            distance = editdistance.eval(query, phrase) / max(len(query), len(phrase))
            best_distance = min(best_distance, distance)
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

