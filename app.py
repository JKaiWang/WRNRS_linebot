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
from questions import LEVEL_1, LEVEL_2, LEVEL_3
from api import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET

app = Flask(__name__)

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

WELCOME_MESSAGE = (
    "歡迎來到 We Are Not Really Strangers 卡牌機器人！\n"
    "請選擇你想要的難度等級：\n"
    "Level 1：破冰 / 第一印象\n"
    "Level 2：深入 / 故事感\n"
    "Level 3：反思 / 情感收尾"
)

LEVEL_SELECTION = TemplateSendMessage(
    alt_text="請選擇難度等級",
    template=ButtonsTemplate(
        title="選擇問題等級",
        text="你想要哪個等級的問題？",
        actions=[
            PostbackAction(label="Level 1 - 破冰", data="LEVEL_1"),
            PostbackAction(label="Level 2 - 深入", data="LEVEL_2"),
            PostbackAction(label="Level 3 - 反思", data="LEVEL_3"),
        ],
    ),
)


def get_random_question(level):
    if level == "LEVEL_1":
        return random.choice(LEVEL_1)
    elif level == "LEVEL_2":
        return random.choice(LEVEL_2)
    elif level == "LEVEL_3":
        return random.choice(LEVEL_3)
    return None


def get_level_name(level):
    level_names = {
        "LEVEL_1": "破冰 / 第一印象",
        "LEVEL_2": "深入 / 故事感",
        "LEVEL_3": "反思 / 情感收尾",
    }
    return level_names.get(level, "")


def create_question_message(level):
    question = get_random_question(level)
    level_name = get_level_name(level)
    return [
        TextSendMessage(
            text=f"🎴 {level_name} 問題：\n\n{question}"
        ),
        TemplateSendMessage(
            alt_text="繼續遊戲",
            template=ButtonsTemplate(
                title="想再抽一張嗎？",
                text="繼續或選擇其他等級",
                actions=[
                    PostbackAction(label="再來一張", data=level),
                    PostbackAction(label="換個等級", data="SELECT_LEVEL"),
                ],
            ),
        ),
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
    if text in ["抽卡", "隨機抽卡", "draw card", "random", "開始"]:
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text=WELCOME_MESSAGE),
                LEVEL_SELECTION,
            ],
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text="我沒有聽懂呢，請輸入「抽卡」來開始！"),
                LEVEL_SELECTION,
            ],
        )


@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    
    if data == "SELECT_LEVEL":
        line_bot_api.reply_message(event.reply_token, LEVEL_SELECTION)
    elif data in ["LEVEL_1", "LEVEL_2", "LEVEL_3"]:
        line_bot_api.reply_message(event.reply_token, create_question_message(data))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
