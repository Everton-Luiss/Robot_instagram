from flask import Flask, request
import telegram
from telebot.credentials import bot_token, bot_user_name,URL
from telebot.mastermind import main

app = Flask(__name__)
@app.route('/respond', methods=['POST'])
def respond():
    print('iniciando')
    return main

@app.route('/')
def index():
    return 'Robot-Instagram'

if __name__ == '__main__':
    app.run(threaded=True)
