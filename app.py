import random
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    PostbackEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    PostbackAction,
)
from questions import QUESTIONS
from api import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET

app = Flask(__name__)

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

WELCOME_MESSAGE = (
    "歡迎來到 We Are Not Really Strangers 卡牌機器人！\n"
    "請點選「隨機抽卡」或輸入「抽卡」來抽一張問題卡。"
)

CARD_BUTTON = TemplateSendMessage(
    alt_text="請選擇隨機抽卡",
    template=ButtonsTemplate(
        title="WNRRS 抽卡",
        text="想要抽一張問題卡嗎？",
        actions=[
            PostbackAction(label="隨機抽卡", data="DRAW_CARD"),
            PostbackAction(label="再抽一次", data="DRAW_CARD"),
        ],
    ),
)


def get_random_question():
    return random.choice(QUESTIONS)


def create_question_message():
    question = get_random_question()
    return [
        TextSendMessage(text=f"🎴 隨機抽卡問題：\n{question}"),
        CARD_BUTTON,
    ]


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


@handler.add(MessageEvent)
def handle_message(event):
    text = event.message.text.strip().lower()
    if text in ["抽卡", "隨機抽卡", "draw card", "random"]:
        line_bot_api.reply_message(event.reply_token, create_question_message())
    else:
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text=WELCOME_MESSAGE),
                CARD_BUTTON,
            ],
        )


@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    if data == "DRAW_CARD":
        line_bot_api.reply_message(event.reply_token, create_question_message())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
