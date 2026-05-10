# WANRS LINE Bot

這是一個 LINE Bot 範例，實現「We Are Not Really Strangers」卡牌遊戲。根據難度等級隨機回傳問題。

## 功能

- 使用者輸入「抽卡」或「隨機抽卡」
- 選擇難度等級：
  - **Level 1 - 破冰**：第一印象，輕鬆開場問題
  - **Level 2 - 深入**：故事感，深層互動問題
  - **Level 3 - 反思**：情感收尾，反思性問題
- 根據選擇的等級隨機回傳一個問題
- 可以繼續抽同等級的卡，或換其他等級

## 安裝

1. 建立虛擬環境（建議）

```bash
python -m venv venv
source venv/bin/activate
```

2. 安裝套件

```bash
pip install -r requirements.txt
```

3. 設定環境變數

建議使用下列 `.env` 範本，不要把真正的金鑰放進版本控制：

```bash
cp .env.example .env
```

然後在你的 shell 裡設定：

```bash
export LINE_CHANNEL_ACCESS_TOKEN="你的 Channel Access Token"
export LINE_CHANNEL_SECRET="你的 Channel Secret"
```


4. 啟動服務

```bash
python app.py
```

5. 設定 LINE 的 Webhook URL

將 LINE 開發者控制台的 Webhook URL 設為：

```
https://你的伺服器地址/callback
```

## 使用方式

- 傳送「抽卡」或「隨機抽卡」
- 點選由 Bot 回應的「隨機抽卡」按鈕

每次抽卡都會得到新的問題。