
from assistant import Assistant
import jieba
from food_stalls import food_stalls
from utilities import parse_number

def order(assistant):
    first_order = True 
    orders = {}
    while(True):
        print("請點餐：") if first_order else print("請繼續點餐：") 
        first_order = False 
        result = None
        while not result:
            result = assistant.listen_and_recognize() 

        if result == u"就這樣":
            break
        else:
            words = list(jieba.cut(result))
            print(''.join(words))
            amount = parse_number(words[0]);
            if amount:
                result = ''.join(words[1:])  
            else:
                amount = 1
            (match, edit_distance) = assistant.search_menu(result)
            if(edit_distance > 0.5):
                print("請問您所說的是 {0} {1}份 嗎？".format(match, amount))
                answer = assistant.confirm()
                if answer:
                    print('{}份 {}'.format(amount, match))
                    if match in orders:
                        orders[match] += amount
                    else:
                        orders[match] = amount
                else:
                    print("好的，讓我們再試一次")
                    continue
            else:
                print('{}份 {}'.format(amount, match))

                if match in orders:
                    orders[match] += amount
                else:
                    orders[match] = amount
    return orders

def sum_orders(menu, orders):
    print("您的訂單：")
    total_price = 0
    for item, amount in orders.items():
        print("{0} {1} 份".format(item, amount))
        total_price += menu[item] * amount 
    return total_price

def initialize_jieba():
    for key, food_stall in food_stalls.items():
        items = tuple(food_stall['menu'].keys())
        if items:
            jieba.suggest_freq(items)

if __name__ == '__main__':
    print("Initialize assistant...", end='')
    assistant = Assistant()
    print("done.")
    print("Initialize jieba...", end='')
    initialize_jieba()
    print("done.")
    
    while True:
        print("想訂哪一家外送?")
        assistant.listen_speech()
        result = None
        while not result:
            result = assistant.listen_and_recognize() 
        (match, edit_distance) = assistant.search_food_stall(result)
        if(edit_distance > 0.5):
            print("請問您所說的是 {0} 嗎？".format(match))
            answer = assistant.confirm()
            
            if answer:
                assistant.food_stall = match
                print("設定店家: {0}".format(match))
                break
            else:
                print("好的，讓我們再試一次")
                continue
        else:
            assistant.food_stall = match
            print("設定店家: {0}".format(match))
            break
    total_price = 0
    minimum_charge = food_stalls[assistant.food_stall]['minimum_charge']
    orders = {}

    while total_price < minimum_charge:
        new_orders = order(assistant)
        for item, amount in new_orders.items():
            if item in orders:
                orders[item] += amount
            else:
                orders[item] = amount

        total_price = sum_orders(food_stalls[assistant.food_stall]['menu'], orders)
        print('總金額為{0}'.format(total_price))

        if total_price < minimum_charge:
            print('還需要 {0} 元才可外送，要再點些什麼嗎？'.format(minimum_charge - total_price))
            answer = assistant.confirm()
            
            if answer:
                print("重新點單")
                continue
            else:
                print("訂單取消")
                exit(0)
    print('為您將訂單送到 {}'.format(assistant.food_stall))
    assistant.send_orders(orders)


    


