from flask import Flask
from logic import check_signals
import threading  # נדרש כדי להריץ את הבוט במקביל
import bot  # נניח שהקובץ שלך נקרא bot.py

app = Flask(__name__)

@app.route('/ping')
def ping():
    result = check_signals()
    return result if result else "✅ נבדק - אין איתות כרגע"

def run_bot():
    bot.run_bot()  # פונקציה שניצור מייד בתוך bot.py

if __name__ == "__main__":
    # הפעלת הבוט בתוך Thread נפרד
    threading.Thread(target=run_bot).start()
    # הפעלת האפליקציה
    app.run(host='0.0.0.0', port=10000)
