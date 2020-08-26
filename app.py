from flask import Flask, request
from telegram.ext import MessageHandler, Filters, Updater, CommandHandler, ConversationHandler
import telegram
import logging
#from telebot.credentials import bot_token, bot_user_name,URL
from telebot.mastermind import (start, begin, reply,reply_senha, cancel, options, comenta_fotos, reply_hash_coment, reply_hashtag_curtir,
curte_fotos, options_follow, reply_follow_profile, follow_by_profile, reply_follow_profile2, follow_by_profile2, options_like, options_coment, reply_num_follow)
from telebot.credentials import bot_token, bot_user_name,URL

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
bot = telegram.Bot(token=TOKEN)

def reply_handler():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), CommandHandler('cancelar', cancel)],
        states={
            BEGIN: [MessageHandler(Filters.text, begin)],
            LOGIN: [MessageHandler(Filters.text, reply)],

            SENHA: [MessageHandler(Filters.text, reply_senha),
                    CommandHandler('cancel', cancel)],
            OPTIONS: [MessageHandler(Filters.text, options)],
            COMENTARIOS: [MessageHandler(Filters.text, comenta_fotos)],
            HASH_COMENT: [MessageHandler(Filters.text, reply_hash_coment)],
            HASH_CURTIR: [MessageHandler(Filters.text, reply_hashtag_curtir)],
            CURTE_FOTOS:[MessageHandler(Filters.text, curte_fotos)],
            OPTIONS_FOLLOW: [MessageHandler(Filters.text, options_follow)],
            FOLLOW_PROFILE: [MessageHandler(Filters.text, reply_follow_profile)],
            FOLLOW_BY_PROFILE: [MessageHandler(Filters.text, follow_by_profile)],
            FOLLOW_PROFILE2: [MessageHandler(Filters.text, reply_follow_profile2)],
            FOLLOW_BY_PROFILE2: [MessageHandler(Filters.text, follow_by_profile2)],
            CANCEL: [MessageHandler(Filters.text, cancel)],
            OPTIONS_LIKE: [MessageHandler(Filters.text, options_like)],
            OPTIONS_COMENT: [MessageHandler(Filters.text, options_coment)],
            NUM_FOLLOW: [MessageHandler(Filters.text, reply_num_follow)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)
    #updater.start_polling()

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return '.'

if __name__ == '__main__':
    app.run(threaded=True)
