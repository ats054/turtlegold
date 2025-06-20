import yfinance as yf
import pandas as pd
from telegram import Bot
from config import TELEGRAM_ID, TELEGRAM_TOKEN
import asyncio

bot = Bot(token=TELEGRAM_TOKEN)

async def async_send(msg):
    await bot.send_message(chat_id=TELEGRAM_ID, text=msg)

def send_alert(msg):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.ensure_future(async_send(msg))
        else:
            loop.run_until_complete(async_send(msg))
    except RuntimeError:
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        new_loop.run_until_complete(async_send(msg))

def check_signals():
    try:
        df = yf.download("GC=F", period="30d", interval="5m", progress=False)
        if df.empty:
            return "⚠️ לא ניתן לטעון נתונים מהשרת (Yahoo Finance)"
        df.dropna(inplace=True)

        last = df.iloc[-1]
        prev = df.iloc[-2]

        # מגמות
        high_20d = df["High"].rolling(window=78*20).max().iloc[-1].item()
        low_20d = df["Low"].rolling(window=78*20).min().iloc[-1].item()

        df['date'] = df.index.date
        yesterday = df[df['date'] < df['date'].max()]
        high_yesterday = yesterday[yesterday['date'] == yesterday['date'].max()].High.max().item()
        low_yesterday = yesterday[yesterday['date'] == yesterday['date'].max()].Low.min().item()

        last_4h = df.iloc[-48:]
        high_4h = last_4h["High"].max().item()
        low_4h = last_4h["Low"].min().item()

        current_price = last["Close"].item()
        plus500_price = current_price - 26.5
        open_price = last["Open"].item()
        high_price = last["High"].item()
        low_price = last["Low"].item()

        reason = None

        # שיטת הצבים (מתוקן)
        if high_price > high_20d:
            reason = "🟢 שבירת שיא 20 ימים"
        elif low_price < low_20d:
            reason = "🔴 שבירת שפל 20 ימים"
        elif high_price > high_yesterday:
            reason = "🟢 שבירת הגבוה של אתמול"
        elif low_price < low_yesterday:
            reason = "🔴 שבירת הנמוך של אתמול"
        elif high_price > high_4h:
            reason = "🟢 שבירת הגבוה של 4 שעות אחרונות"
        elif low_price < low_4h:
            reason = "🔴 שבירת השפל של 4 שעות אחרונות"

        # שיטת נרות - עם high ו-low במקום close
        elif high_price > open_price and (high_price - open_price) > (high_price - low_price) * 0.6:
            reason = "📊 🟢 נר שורי חזק (Bullish Candle)"
        elif low_price < open_price and (open_price - low_price) > (high_price - low_price) * 0.6:
            reason = "📊 🔴 נר דובי חזק (Bearish Candle)"
       
        if reason:
            msg = f"""📢 איתות זהב לפי ניתוח יומי

📈 מחיר נוכחי: ${current_price:.2f}
📉 מחיר בפלוס500: ${plus500_price:.2f}
🔍 סיבה: {reason}

⏱️ נבדק אוטומטית כל 5 דקות.
"""
            send_alert(msg)
            return msg

        return "✅ נבדק - אין איתות כרגע"

    except Exception as e:
        return f"❌ שגיאה במהלך הבדיקה: {str(e)}"
