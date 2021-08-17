# line-bot聊天機器人

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)

# 載入linebot.models的功能，如要增加StickerSendMessage功能，就要加進去
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
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
    msg = event.message.text # 使用者所傳的文字
    r = '後看不懂你說什麼?!' # 預設要回的文字

    if '給我貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='11537',
            sticker_id='52002735'
        )

        line_bot_api.reply_message(
            event.reply_token,
            sticker_message)
        return

    if msg in ['hi','Hi','HI']:
        r = '嗨!! 你好哦'
    elif msg == '你吃飯了嗎':
        r = '我還沒吃飯，都快餓死了 >_<lll'
    elif msg == '你是誰':
        r = '我是Chien的機器人'
    elif '訂位' in msg:
        r = '你想訂位嗎? 要訂幾點的呢?'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r)) # 回傳使用者的文字


if __name__ == "__main__": # 當直接被執行時，就執行以下程式
    app.run()
