from flask import Flask, request
from telegram.ext import MessageHandler, Filters, Updater, CommandHandler, ConversationHandler
import telegram
import logging
#from telebot.credentials import bot_token, bot_user_name,URL
from telebot.mastermind import (start, begin, reply,reply_senha, cancel, options, comenta_fotos, reply_hash_coment, reply_hashtag_curtir,
curte_fotos, options_follow, reply_follow_profile, follow_by_profile, reply_follow_profile2, follow_by_profile2, options_like, options_coment, reply_num_follow)

TOKEN = '11368978547:AAEoYdgxdm586q7tcF1xQT3OpL3SBZBNLT0'
bot = telegram.Bot(token=TOKEN)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)
OPTIONS, BEGIN, LOGIN, SENHA, COMENTARIOS, HASH_COMENT, HASH_CURTIR, CURTE_FOTOS, OPTIONS_FOLLOW, FOLLOW_PROFILE,\
FOLLOW_BY_PROFILE, FOLLOW_PROFILE2, FOLLOW_BY_PROFILE2, CANCEL, OPTIONS_LIKE, OPTIONS_COMENT, NUM_FOLLOW = range(17)

app = Flask(__name__)

@app.route('/hook', methods=['POST'])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)

    return 'ok'

@app.route('/')
def index():
    return '.'

if __name__ == '__main__':
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
            CURTE_FOTOS: [MessageHandler(Filters.text, curte_fotos)],
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
    #app.run(threaded=True)
