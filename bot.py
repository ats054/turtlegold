from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
from config import TELEGRAM_TOKEN
from logic import check_signals  # הפונקציה שכבר יש לך

def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("🔄 רענן עכשיו", callback_data='refresh')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('👋 הבוט פעיל! לחץ על הכפתור לבדיקה מיידית:', reply_markup=reply_markup)

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == 'refresh':
        result = check_signals()
        query.edit_message_text(text=f'🔍 תוצאה:\n\n{result}')

def run_bot():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button_handler))

    updater.start_polling()
    updater.idle()
