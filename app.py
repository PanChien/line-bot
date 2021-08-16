# line-bot聊天機器人

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('9jcEvoPECjBvGsKEvZYi7fUISRhIAs+ZZ2z5vh1JzwVnkxxuNosU1SqLUYh2SBDGWKuDLxFVwYJn03WekbpkRtbZzJDNELQtvF0GDDXhfBRcM196AHw/6BCVzcS6fKRZWrqA5GzLeec3J6ZJRrLVCwdB04t89/1O/w1cDnyilFU=') # channel access token
handler = WebhookHandler('f2fd8331377880b9e3b89a3ba319663c') # channel secret

# 當line機器人收到訊息後，line轉載到我們的伺服器，會先觸發以下程式
@app.route("/callback", methods=['POST']) # route路徑，line公司轉載網址有/callback時，就會執行以下程式
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# 上面的程式，會再觸發下面的程式
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)) # 回傳使用者的文字


if __name__ == "__main__": # 當直接被執行時，就執行以下程式
    app.run()
