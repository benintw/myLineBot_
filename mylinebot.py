

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, StickerSendMessage,
    LocationSendMessage, QuickReply,QuickReplyButton, MessageAction, AudioSendMessage,
    VideoSendMessage, 
)

from linebot.models import (
    PostbackEvent, TextSendMessage, TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, PostbackTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn,
    ImageCarouselTemplate, ImageCarouselColumn
)
from urllib.parse import parse_qsl



app = Flask(__name__)

CHANNEL_SECRET = '63edf9a6d2a1ae59e1d9108f0bcfb8ad'
CHANNEL_ACCESS_TOKEN = "dRkGyKcQ18qxOJtyvLiyQGC/0YN2PY3sSCOzFOEDmuazFk+WZ+Nk1OfyclOGbVm9MhdBHoXKHWfppxWLeY4HD/2RMevx9Co+Rk9/Yjh610yMF759dYBN0lrYdmKxhfllApY5dRAzltJfWBl4ouNZ7QdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
line_bot_api.push_message("U2753d6c06c557ace8c2fc8b1e2808d4b", TextSendMessage(text='testlineBOT 來溜'))

@app.route("/callback", methods=['POST'])
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



baseurl = 'https://d25a-115-43-147-119.jp.ngrok.io/static/'
pizza_url = "https://i.imgur.com/4QfKuz1.png"
lbj_url = "https://i.imgur.com/ARO7AAa.jpeg" 



# 回應訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
    
    # Testing 傳送文字
    if mtext == '@傳送文字':
        try:
            message = TextSendMessage(text = "這是測試文字08-11-3:30")
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(
                text="發生錯誤!"
            ))

    # 傳送位置
    elif mtext == '@傳送位置':
        try:
            message = LocationSendMessage(
                title = "團練 Fitopia",
                address = "235新北市中和區景平路690號",
                # 25.00175241122356, 121.49698463408848
                latitude = 25.00175241122356, # 緯度
                longitude = 121.49698463408848 # 精度
            )
            
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(
                text="發生錯誤!"
            ))

    # 快速選單
    if mtext == '@快速選單':
        try:
            message = TextSendMessage(
                text = '請選擇想聯絡的教練',
                quick_reply = QuickReply(
                    items = [
                        QuickReplyButton(
                            action = MessageAction(label='黑悟空', text="Zat")
                        ),
                        QuickReplyButton(
                            action = MessageAction(label="奇諾", text = "Kino")
                        ),
                        QuickReplyButton(
                            action = MessageAction(label='五股王陽明', text = "Vincent")
                        ),
                        QuickReplyButton(
                            action = MessageAction(label='勇迷', text="Jason")
                        ),
                        QuickReplyButton(
                            action = MessageAction(label='志偉', text='志偉')
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(
                text="發生錯誤!"
            ))



    # 
    if mtext == "@按鈕樣板":
        sendButton(event)
    
    elif mtext == "@確認樣板":
        sendConfirm(event)
    
    elif mtext == "@轉盤樣板":
        sendCarousel(event)
    
    elif mtext == "@圖片轉盤":
        sendImgCarousel(event)
    
    elif mtext == "@購買披薩":
        sendPizza(event)
    
    elif mtext == "@yes":
        sendYes(event)

@handler.add(PostbackEvent) # PostbackTemplateAction會觸發此事件
def handle_postback(event):
    backdata = dict(parse_qsl(event.postback.data)) # 取得postback資料
    if backdata.get('action') == 'buy':
        # message = TextSendMessage(
        #     text = '感謝您購買披薩, 正在做了, 吵屁'
        # )
        # line_bot_api.reply_message(event.reply_token, message)
        sendBack_buy(event, backdata)
    elif backdata.get("action") == 'sell':
        sendBack_sell(event, backdata)



def sendBack_buy(event, backdata):
    try:
        text1 = 'sendBack_buy 觸發, \n(action的值為'+ backdata.get("action")+ ')'
        text1 += '\n可將處理程式寫在此處'
        message = TextSendMessage(
            text = text1
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="sendBack_buy 發生錯誤"))

def sendBack_sell(event, backdata): # 處理 postback
    try:
        message = TextSendMessage(
            text = '點選的是賣'+backdata.get("item")
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="sendBack_sell 發生錯誤"))


def sendButton(event): # 按鈕樣板
    try:
        message = TemplateSendMessage(
            alt_text = "按鈕樣板",
            template = ButtonsTemplate(
                thumbnail_image_url = pizza_url, # 顯示的圖片
                title = "按鈕樣板示範",
                text = "請選擇",
                actions = [
                    MessageTemplateAction(
                        label = '文字訊息-要買披薩嗎?',
                        text = "@購買披薩"
                    ),
                    URITemplateAction(
                        label = '網頁連結', # 按鈕文字
                        uri = "https://www.facebook.com/FITOPIA2021/" # 網址
                    ),
                    PostbackTemplateAction( # 執行postback 功能, 觸發postback事件
                        label = '回傳訊息', #按鈕文字
                        text = "這段text可以省略掉 ", # 如果不需要使用者看到回傳的文字訊息,這邊可以省去text
                        data = 'action=buy'
                    ),
                ]

            )
        )
        line_bot_api.reply_message(event.reply_token,message)

    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='sendButton 發生錯誤!!!!'))


def sendPizza(event):
    try:
        message = TextSendMessage(
            text = "sendPizza 方法觸發, 我他媽正在做了, 等"
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='sendPizza 發生錯誤! '))

def sendConfirm(event):
    try:
        message = TemplateSendMessage(
            alt_text = '確認樣板',
            template = ConfirmTemplate(
                text = '確認你要買這個嗎?',
                actions = [
                    MessageTemplateAction(
                        label = '對啦',
                        text = "@yes"
                    ),
                    MessageTemplateAction(
                        label = '否, 我不買這爛東西',
                        text = "@no"
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='sendConfirm 發生錯誤! '))



def sendYes(event):
    try:
        message = TextSendMessage(
            text = '感謝您的購買,\n我們會盡快寄出商品. '
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='sendYes 發生錯誤! '))


# 轉盤樣板
def sendCarousel(event):
    try:
        message = TemplateSendMessage(
            alt_text = '轉盤樣板',
            template = CarouselTemplate(
                columns = [
                    CarouselColumn(
                        thumbnail_image_url = pizza_url,
                        title = '這是樣板 1',
                        text = ' 第一個轉盤樣板',
                        actions = [
                            MessageTemplateAction(
                                label = '文字訊息一',
                                text = '賣披薩'
                            ),
                            URITemplateAction(
                                label = 'Fitopia健身房',
                                uri = "https://www.facebook.com/FITOPIA2021"
                            ),
                            PostbackTemplateAction(
                                label = '回傳訊息一',
                                data = 'action=sell&item=披薩'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url = lbj_url,
                        title = '這是模板二',
                        text = '第二個轉盤樣板',
                        actions = [
                            MessageTemplateAction(
                                label = '文字訊息二',
                                text = '賣飲料'
                            ),
                            URITemplateAction(
                                label = 'Data Science Meetup',
                                uri = "https://www.facebook.com/groups/1356636874425968?hoisted_section_header_type=recently_seen&multi_permalinks=5413765362046412"
                            ),
                            PostbackTemplateAction(
                                label = '回傳訊息二',
                                data = 'action=sell&item=飲料'
                            ),
                        ]

                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='sendCarousel發生錯誤'))       

# 圖片裝盤樣板
def sendImgCarousel(event):
    try:
        message = TemplateSendMessage(
            alt_text = '圖片轉盤樣版',
            template = ImageCarouselTemplate(
                columns = [
                    ImageCarouselColumn(
                        image_url = pizza_url,
                        action = MessageTemplateAction(
                            label = '選披薩',
                            text = 'text = 賣披薩'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url = lbj_url,
                        action = PostbackTemplateAction(
                            label = '回傳訊息',
                            data = 'action=sell&item=飲料'
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='sendImgCarousel發生錯誤'))



# if __name__ == "__main__":
#     app.run()


# 每次run完要去要去line Developers 更新 Webhook URL (ngrok tunnel) ＋/callback

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)