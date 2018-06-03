
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage)
from constants import (LINE_CHANNEL_TOKEN, LINE_CHANNEL_SECRET)

# initialize 
line_bot_api = LineBotApi(LINE_CHANNEL_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

def line_send_to(id, message):
    line_bot_api.push_message(id, TextSendMessage(text=message))
