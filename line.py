
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage)
from constants import (LINE_CHANNEL_TOKEN, LINE_CHANNEL_SECRET, LINE_USER_ID)

# initialize 
line_bot_api = LineBotApi(LINE_CHANNEL_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

def line_send_to(id = LINE_USER_ID, message = '' ):
    line_bot_api.push_message(id, TextSendMessage(text=message))
