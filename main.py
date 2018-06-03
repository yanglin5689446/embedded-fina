
from recognizer import Recognizer
from line import line_send_to
import jieba

if __name__ == '__main__':
    print("Initialize recognizer...")
    print("Calibrating microphone...") 
    recognizer = Recognizer()
    print("想點哪一家外送?")
    recognizer.listen_speech()
    result = recognizer.recognize_audio()
    print("設定店家: {0}".format(result))
    first_order = False
    all_orders = []
    while(True):
        print("請點餐：") if first_order else print("請繼續點餐：") 
        recognizer.listen_speech()
        result = recognizer.recognize_audio()
        if result == u"就這樣":
            break
        else:
            if result:
                print("新增項目: {0}".format(result))
                all_orders.append(result)
    print("您的訂單：")
    print(all_orders)
