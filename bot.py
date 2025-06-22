from telegram.ext import Updater, CommandHandler
from config import TELEGRAM_TOKEN, TELEGRAM_ID

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="✅ הבוט פועל!")

def run_bot():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()  # ישאיר את הבוט פעיל
