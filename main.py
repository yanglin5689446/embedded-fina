
from assistant import Assistant
import jieba
from food_stalls import food_stalls
from utilities import parse_number
from time import time

def order(assistant):
    first_order = True 
    orders = {}
    orders_stack = []
    while(True):
        assistant.say("請點餐：") if first_order else assistant.say("請繼續點餐：") 
        first_order = False 
        result = None
        while not result:
            result = assistant.listen_and_recognize() 

        if assistant.check_order_finish(result):
            break
        
        if assistant.check_cancel(result):
            assistant.say("取消上一次訂單")
            if len(orders_stack):
                last_order = orders_stack.pop()
                orders[last_order['name']] -= last_order['amount']
            continue
        
        print(result)
        words = list(jieba.cut(result))
        amount = parse_number(words[0]);
        if amount:
            result = ''.join(words[1:])  
        else:
            amount = 1
        (match, edit_distance) = assistant.search_menu(result)
        if(edit_distance > 0.5):
            assistant.say("請問您所說的是 {0} {1}份 嗎？".format(match, amount))
            answer = assistant.confirm()
            if answer:
                assistant.say('{}份 {}，收到'.format(amount, match))
                orders_stack.append({ 'name': match, 'amount': amount})
                if match in orders:
                    orders[match] += amount
                else:
                    orders[match] = amount
            else:
                assistant.say("好的，請再試一次")
                continue
        elif edit_distance >= 1.0:
            assistant.say("抱歉，我不了解您說的品項")
            continue
        else:
            assistant.say('{}份 {}，收到'.format(amount, match))
            orders_stack.append({ 'name': match, 'amount': amount})

            if match in orders:
                orders[match] += amount
            else:
                orders[match] = amount
    return orders

def sum_orders(assistant, menu, orders):
    assistant.say("您的訂單：")
    total_price = 0
    for item, amount in orders.items():
        assistant.say("{0} {1} 份".format(item, amount))
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
        assistant.say("想訂哪一家外送?")
        result = None
        while not result:
            result = assistant.listen_and_recognize() 
        (match, edit_distance) = assistant.search_food_stall(result)
        if(edit_distance > 0.5):
            assistant.say("請問您所說的是 {0} 嗎？".format(match))
            answer = assistant.confirm()
            
            if answer:
                assistant.food_stall = match
                assistant.say("設定店家: {0}".format(match))
                break
            else:
                assistant.say("好的，請再試一次")
                continue
        else:
            assistant.food_stall = match
            assistant.say("設定店家: {0}".format(match))
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

        total_price = sum_orders(assistant, food_stalls[assistant.food_stall]['menu'], orders)
        assistant.say('總金額為{0}元'.format(total_price))

        if total_price < minimum_charge:
            assistant.say('還需要 {0} 元才可以外送，要再點些什麼嗎？'.format(minimum_charge - total_price))
            answer = assistant.confirm()
            
            if answer:
                assistant.say("重新點單")
                continue
            else:
                assistant.say("訂單取消")
                exit(0)
    assistant.say('是否要為您將訂單送到 {}？'.format(assistant.food_stall))
    answer = assistant.confirm()
    if answer:
        assistant.say('為您將訂單送到 {}'.format(assistant.food_stall))
    else:
        file_name = "order-{}.txt".format(time())
        print("將點餐結果匯出至 {}".format(file_name))

        with open(file_name, 'w') as f:
            for item, amount in orders.items():
                f.write("{0} {1} 份\n".format(item, amount))
        assistant.send_orders(orders)


    


