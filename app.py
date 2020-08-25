from flask import Flask, request
import telegram
#from telebot.credentials import bot_token, bot_user_name,URL
from telebot.mastermind import main

TOKEN = '11368978547:AAEoYdgxdm586q7tcF1xQT3OpL3SBZBNLT0'
URL = 'https://robot-instagran.herokuapp.com/'

app = Flask(__name__)
@app.route('/respond', methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    text = update.message.text.encode('utf-8').decode()
    print("got text message :", text)
    if text == '/start':
        print(iniciando)
        return main
    else:
        bot_error = 'Digite /start'
        bot.sendMessage(chat_id=chat_id, text=bot_error, reply_to_message_id=msg_id)

    return 'OK go!'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return 'Robot-Instagram'

if __name__ == '__main__':
    app.run(threaded=True)
