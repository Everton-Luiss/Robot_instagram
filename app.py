from flask import Flask, request
from telegram.ext import MessageHandler, Filters, Updater, CommandHandler, ConversationHandler
import telegram
#from telebot.credentials import bot_token, bot_user_name,URL
from telebot.mastermind import main

app = Flask(__name__)

@app.route('/respond')
def respond():
    print('iniciando')
    return main

@app.route('/')
def index():
    return '.'


if __name__ == '__main__':
    app.run(threaded=True)
