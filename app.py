from flask import Flask, request
import telegram
#from telebot.credentials import bot_token, bot_user_name,URL
from telebot.mastermind import main

#TOKEN = '11368978547:AAEoYdgxdm586q7tcF1xQT3OpL3SBZBNLT0'
#URL = 'https://robot-instagran.herokuapp.com/'

app = Flask(__name__)
#@app.route('/{}'.format(TOKEN), methods=['POST'])
@app.route('/respond', methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    print("got text message :", text)

    response = main()
    bot.sendMessage(chat_id=chat_id, text=response)

    return 'ok'


''' print('iniciando')
    return main'''

@app.route('/')
def index():
    return 'Robot-Instagram'

if __name__ == '__main__':
    app.run(threaded=True)
