from flask import Flask, request
from telegram.ext import MessageHandler, Filters, Updater, CommandHandler, ConversationHandler
import telegram
import logging
#from telebot.credentials import bot_token, bot_user_name,URL
from telebot import mastermind

TOKEN = '11368978547:AAEoYdgxdm586q7tcF1xQT3OpL3SBZBNLT0'
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)

@app.route('/')
def index():
    return 'Robot-Instagram'


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), CommandHandler('cancelar', cancel)],
        states={
            BEGIN: [MessageHandler(Filters.text, mastermind.begin)],
            LOGIN: [MessageHandler(Filters.text, mastermind.reply)],

            SENHA: [MessageHandler(Filters.text, mastermind.reply_senha),
                    CommandHandler('cancel', mastermind.cancel)],
            OPTIONS: [MessageHandler(Filters.text, mastermind.options)],
            COMENTARIOS: [MessageHandler(Filters.text, mastermind.comenta_fotos)],
            HASH_COMENT: [MessageHandler(Filters.text, mastermind.reply_hash_coment)],
            HASH_CURTIR: [MessageHandler(Filters.text, mastermind.reply_hashtag_curtir)],
            CURTE_FOTOS:[MessageHandler(Filters.text, mastermind.curte_fotos)],
            OPTIONS_FOLLOW: [MessageHandler(Filters.text, mastermind.options_follow)],
            FOLLOW_PROFILE: [MessageHandler(Filters.text, mastermind.reply_follow_profile)],
            FOLLOW_BY_PROFILE: [MessageHandler(Filters.text, mastermind.follow_by_profile)],
            FOLLOW_PROFILE2: [MessageHandler(Filters.text, mastermind.reply_follow_profile2)],
            FOLLOW_BY_PROFILE2: [MessageHandler(Filters.text, mastermind.follow_by_profile2)],
            CANCEL: [MessageHandler(Filters.text, mastermind.cancel)],
            OPTIONS_LIKE: [MessageHandler(Filters.text, options_like)],
            OPTIONS_COMENT: [MessageHandler(Filters.text, mastermind.options_coment)],
            NUM_FOLLOW: [MessageHandler(Filters.text, mastermind.reply_num_follow)],
    },
    fallbacks=[CommandHandler('start', mastermind.cancel)]
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()

if __name__ == '__main__':
    app.run(threaded=True)
