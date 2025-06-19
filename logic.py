import yfinance as yf
import pandas as pd
from telegram import Bot
from config import TELEGRAM_ID, TELEGRAM_TOKEN

bot = Bot(token=TELEGRAM_TOKEN)

def send_alert(msg):
    bot.send_message(chat_id=TELEGRAM_ID, text=msg)

def check_signals():
    df = yf.download("GC=F", period="30d", interval="5m")
    df.dropna(inplace=True)
    last = df.iloc[-1]
    high_20d = df["High"].rolling(window=78*20).max().iloc[-1]
    low_20d = df["Low"].rolling(window=78*20).min().iloc[-1]
    df['date'] = df.index.date
    yesterday = df[df['date'] < df['date'].max()]
    high_yesterday = yesterday[yesterday['date'] == yesterday['date'].max()].High.max()
    low_yesterday = yesterday[yesterday['date'] == yesterday['date'].max()].Low.min()
    last_4h = df.iloc[-48:]
    high_4h = last_4h["High"].max()
    low_4h = last_4h["Low"].min()

    current_price = last["Close"]
    plus500_price = current_price - 26.5

    reason = None
    if current_price > high_20d:
        reason = "שבירת שיא 20 ימים"
    elif current_price < low_20d:
        reason = "שבירת שפל 20 ימים"
    elif current_price > high_yesterday:
        reason = "שבירת הגבוה של אתמול"
    elif current_price < low_yesterday:
        reason = "שבירת הנמוך של אתמול"
    elif current_price > high_4h:
        reason = "שבירת הגבוה של 4 שעות אחרונות"
    elif current_price < low_4h:
        reason = "שבירת השפל של 4 שעות אחרונות"

    if reason:
        msg = f"""
📢 איתות זהב לפי שיטת הצבים

📈 מחיר נוכחי: ${current_price:.2f}
📉 מחיר בפלוס500: ${plus500_price:.2f}
🔍 סיבה: {reason}

⏱️ נבדק אוטומטית כל 5 דקות.
"""
        send_alert(msg)
        return msg
    return None