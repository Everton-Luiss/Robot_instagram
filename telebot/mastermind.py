from telegram.ext import MessageHandler, Filters, Updater, CommandHandler, ConversationHandler
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import logging
import time
import random
import os
from flask import Flask, request, make_response
import json

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)
OPTIONS, BEGIN, LOGIN, SENHA, COMENTARIOS, HASH_COMENT, HASH_CURTIR, CURTE_FOTOS, OPTIONS_FOLLOW, FOLLOW_PROFILE,\
FOLLOW_BY_PROFILE, FOLLOW_PROFILE2, FOLLOW_BY_PROFILE2, CANCEL, OPTIONS_LIKE, OPTIONS_COMENT, NUM_FOLLOW = range(17)
data = []

def get_response(msg):
    return start

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Olá, me chamo Ana. Sou seu robô assistente e vou te ajudar a ter mais seguidores no instagram! Vamos começar?")
    return BEGIN

def begin(update, context):
    response_begin = (update.message.text).upper()
    if response_begin == "SIM" or response_begin == "VAMOS" or response_begin == "S":
        resp = "Então vamos! \n\nPor favor, digite seu login:."
        update.message.reply_text(resp)
        return LOGIN
    if response_begin == "NÃO" or response_begin == "N":
        context.bot.send_message(chat_id=update.effective_chat.id, text="Até logo!")
        return ConversationHandler.END
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Desculpe, não entendi! Digite /start para reiniciar.")
        return ConversationHandler.END


def login(user_input):
    answer = "Seu login é: " + user_input + '. \n\nAgora digite sua senha: \n\n(para sair digite /cancel)'
    data.insert(0, user_input)
    print(data[0])
    return answer

def reply(update, context):
    user_input = update.message.text
    update.message.reply_text(login(user_input))
    return SENHA

def senha(user_senha):
    answer_senha = ("Sua senha é: " + user_senha + ". \n\nVoce deseja seguir, curtir ou comentar?\n\n "
                    "Digite 1 para seguir, 2 para curtir e 3 para comentar")
    data.insert(1, user_senha)
    print(data[1])
    return answer_senha

def reply_senha(update, context):
    user_senha = update.message.text
    update.message.reply_text(senha(user_senha))
    return OPTIONS

def options(update, context):
    response = update.message.text
    if response == "1":
        say_1 = "Você deseja seguir quantas pessoas?"
        '''say_1 = "Você deseja seguir pessoas por perfil, sugeridos ou localização?\n\n"\
                "Digite 1 para seguir por sugeridos\n" \
                "Digite 2 para seguir por perfil e sugeridos \n" \
                "Digite 3 para seguir por perfil\n" \
                "Digite 4 para seguir por localização\n" \
                "Para cancelar digite sair"'''
        update.message.reply_text(say_1)
        return NUM_FOLLOW
    elif response == "2":
        say_2 = "Você deseja curtir fotos do feed ou de alguma hashtag?\n\n" \
                "Digite 1 para curtir fotos do feed\n" \
                "Digite 2 para curtir fotos de alguma hashtag\n" \
                "Para cancelar digite sair"
        update.message.reply_text(say_2)
        return OPTIONS_LIKE
    elif response == "3":
        say_3 = "Você deseja comentar fotos do feed ou de alguma hashtag?\n\n"\
                "Digite 1 para comentar fotos do feed\n" \
                "Digite 2 para comentar fotos de alguma hashtag\n" \
                "Para cancelar digite sair"
        update.message.reply_text(say_3)
        return OPTIONS_COMENT
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Desculpe, não entendi. Vou repetir as opções:\n\n Digite 1 para seguir, 2 para curtir e 3 para comentar")
        data.clear()
        return OPTIONS

def num_follow(user_num_follow):
    answer_num = "Entendi, você deseja seguir "+ user_num_follow + " pessoas.\n\n" \
               "Você deseja seguir pessoas por perfil, sugeridos ou localização?\n\n" \
               "Digite 1 para seguir por sugeridos\n" \
               "Digite 2 para seguir por perfil e sugeridos \n" \
               "Digite 3 para seguir por perfil\n" \
               "Digite 4 para seguir por localização\n" \
               "Para cancelar digite sair"
    data.insert(2, user_num_follow)
    print(data[2])
    return answer_num

def reply_num_follow(update, context):
    user_num_follow = update.message.text
    update.message.reply_text(num_follow(user_num_follow))
    return OPTIONS_FOLLOW

def options_coment(update, context):
    response_option_follow = (update.message.text).upper()
    if response_option_follow == "1":
        context.bot.send_message(chat_id=update.effective_chat.id, text="Então vamos começar...")
        time.sleep(2)
        count_coment = 0
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        #driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        driver = webdriver.Chrome(executable_path="/home/tom/PycharmProjects/Bot/mastermind/chromedriver")
        driver.get("https://instagram.com")
        time.sleep(2)
        list_no_repetition = []
        try:
            driver.find_element_by_xpath("//input[@name=\"username\"]") \
                .send_keys(data[0])
            driver.find_element_by_xpath("//input[@name=\"password\"]") \
                .send_keys(data[1])
            driver.find_element_by_xpath('//button[@type="submit"]') \
                .click()
            time.sleep(3)
        except Exception as erro:
            print(erro)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Deu ruim: Eu acho que você pode ter errado seus dados ou sua internet está instável\n\n" \
                                          f"Bora de novo?")
            return BEGIN
        try:
            for c in range(2):
                driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]") \
                    .click()
                time.sleep(2)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Eu tô dando uma olhada aqui no seu feed procurando as melhores fotos pra comentar...\n\n"\
                                          f"Como sou um robô muito jovem não tenho um grande vocabulário. Por isso vou fazer comentários do tipo:\n\n"\
                                          f"Arrazou!, Foto linda!, Adorei, Muito bom!, Paid'édua, s2\n\n"\
                                          f"Em breve você poderá adicionar uma lista com os comentários que você deseja fazer\n\n"\
                                          f"Aaah! mais uma coisa: Não se preocupe com bloqueio por ação de bot porque eu digito igualzinho um ser humano! :)")
            for p in range(5):
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(3)
            tag_a = driver.find_elements_by_tag_name('a')
            profile_hrefs = [elem.get_attribute('href') for elem in tag_a]
            for i in profile_hrefs:
                if i not in list_no_repetition:
                    list_no_repetition.append(i)
            print(str(len(profile_hrefs)))
            print(profile_hrefs)
            print(list_no_repetition)
            time.sleep(3)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Olha que paid'égua: encontrei {len(list_no_repetition)} fotos pra comentar")
            for profile in list_no_repetition:
                driver.get(profile)
                time.sleep(3)
                driver.find_element_by_xpath('//div[@class="_9AhH0"]') \
                    .click()
                time.sleep(2)
                lista = ["Arrazou!", "Foto linda!!", "Adorei", "Muito bom!", "Paid'édua", "s2"]
                driver.find_element_by_class_name("Ypffh").click()
                campo_comentario = driver.find_element_by_class_name("Ypffh")
                time.sleep(random.randint(2, 5))
                c = random.choice(lista)
                for letra in c:
                    campo_comentario.send_keys(letra)
                    time.sleep(random.randint(1, 5) / 30)
                time.sleep(random.randint(5, 7))
                campo_comentario.send_keys(Keys.RETURN)
                count_coment+=1
                time.sleep(5)
        except Exception as e:
            context.bot.send_message(chat_id=update.effective_chat.id,text=f"Erro: {e}")
            print(e)
        finally:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Acabei fazer {count_coment} comentários em fotos do seu feed. Deseja fazer mais alguma coisa?\n\n" \
                                          "Digite 1 para seguir, 2 para curtir e 3 para comentar")
            return OPTIONS
    elif response_option_follow == '2':
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Você deseja comentar fotos de qual hashtag? ")
        return HASH_COMENT
    elif response_option_follow == 'SAIR':
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Pena que você já vai.\n\n Se precisar de min é só chamar")
        data.clear()
        return ConversationHandler.END
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Desculpe, não entendi. Vou repetir as opções:\n\n"
                                      "Digite 1 para comentar fotos do feed\n" \
                                      "Digite 2 para comentar fotos de alguma hashtag\n"
                                      "Para cancelar digite sair")
        return OPTIONS_COMENT

def comenta_fotos(update,context):
    response_hashtag = (update.message.text).upper()
    if response_hashtag == "SIM" or response_hashtag == "S" or response_hashtag == "PODEMOS":
        context.bot.send_message(chat_id=update.effective_chat.id, text="Então vamos começar...")
        time.sleep(2)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        #driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        driver = webdriver.Chrome(executable_path="/home/tom/PycharmProjects/Bot/mastermind/chromedriver")
        driver.get("https://instagram.com")
        time.sleep(2)
        count_coment=0
        list_no_repetition = []
        try:
            driver.find_element_by_xpath("//input[@name=\"username\"]") \
                .send_keys(data[0])
            driver.find_element_by_xpath("//input[@name=\"password\"]") \
                .send_keys(data[1])
            driver.find_element_by_xpath('//button[@type="submit"]') \
                .click()
            time.sleep(3)
        except Exception as erro:
            print(erro)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Deu ruim: Eu acho que você pode ter errado seus dados ou sua internet está instável\n\n" \
                                          f"Bora de novo?")
            return BEGIN
        try:
            driver.get("https://www.instagram.com/explore/tags/" + data[2] + "/")
            time.sleep(3)
            for c in range(4):
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(3)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Eu tô dando uma olhada aqui na hashtag {data[2]} procurando as melhores fotos pra comentar...\n\n" \
                                          f"Como sou um robô muito jovem não tenho um grande vocabulário. Por isso vou fazer comentários do tipo:\n\n" \
                                          f"Arrazou!, Foto linda!, Adorei, Muito bom!, Paid'édua, s2...\n\n" \
                                          f"Em breve você poderá adicionar uma lista com os comentários que você deseja fazer\n\n" \
                                          f"Aaah! mais uma coisa: Não se preocupe com bloqueio por ação de bot porque eu digito igualzinho um ser humano! :)")
            hrefs = driver.find_elements_by_tag_name("a")
            pic_hrefs = [elem.get_attribute("href") for elem in hrefs]
            for i in pic_hrefs:
                if i not in list_no_repetition:
                    list_no_repetition.append(i)
            print(str(len(pic_hrefs)))
            print(pic_hrefs)
            print(list_no_repetition)
            time.sleep(3)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Olha que paid'égua: encontrei {len(list_no_repetition)} fotos pra comentar")
            for pic in list_no_repetition:
                driver.get(pic)
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                lista = ["Arrazou!", "Foto linda!!", "Adorei", "Muito bom!", "Paid'édua", "s2", ]
                driver.find_element_by_class_name("Ypffh").click()
                campo_comentario = driver.find_element_by_class_name("Ypffh")
                time.sleep(random.randint(2, 5))
                c = random.choice(lista)
                for letra in c:
                    campo_comentario.send_keys(letra)
                    time.sleep(random.randint(1, 5) / 30)
                time.sleep(random.randint(5, 7))
                campo_comentario.send_keys(Keys.RETURN)
                count_coment+=1
                time.sleep(5)
        except Exception as e:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Erro: {e}")
            print(e)
        finally:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Acabei fazer {count_coment} comentários em fotos da hashtag {data[2]}. Deseja fazer mais alguma coisa?\n\n" \
                                          "Digite 1 para seguir, 2 para curtir e 3 para comentar")
            return OPTIONS
    elif response_hashtag == "NÃO" or response_hashtag == "N":
        context.bot.send_message(chat_id=update.effective_chat.id, text="Até logo!")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Desculpe, não entendi. Vou repetir as opções:\n\n"
                                      "Digite 1 para comentar fotos do feed\n" \
                                      "Digite 2 para comentar fotos de alguma hashtag\n\n"
                                      "Para cancelar digite sair")
        return OPTIONS_COMENT

def hash_coment(user_hashtag):
    answer_hashtag = "Você deseja pesquisar por: #"+ user_hashtag + ".\n\n Podemos começar?"
    data.insert(2, user_hashtag)
    print(data[2])
    return answer_hashtag

def reply_hash_coment(update, context):
    user_hashtag = update.message.text
    update.message.reply_text(hash_coment(user_hashtag))
    return COMENTARIOS

def options_like(update, context):
    response_option_follow = (update.message.text).upper()
    if response_option_follow == "1":
        context.bot.send_message(chat_id=update.effective_chat.id, text="Então vamo arrochaaaar...")
        time.sleep(2)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        #driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        driver = webdriver.Chrome(executable_path="/home/tom/PycharmProjects/Bot/mastermind/chromedriver")
        driver.get("https://instagram.com")
        time.sleep(2)
        list_no_repetition = []
        count_like = 0
        try:
            driver.find_element_by_xpath("//input[@name=\"username\"]") \
                .send_keys(data[0])
            driver.find_element_by_xpath("//input[@name=\"password\"]") \
                .send_keys(data[1])
            driver.find_element_by_xpath('//button[@type="submit"]') \
                .click()
            time.sleep(3)
        except Exception as erro:
            print(erro)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"Deu ruim: Eu acho que você pode ter errado seus dados ou sua internet está instável\n\n" \
                                      f"Bora de novo?")
            return BEGIN
        try:
            for c in range(2):
                driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]") \
                    .click()
                time.sleep(2)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Eu tô dando uma olhada aqui no seu feed procurando as melhores fotos pra curtir...")
            for p in range(5):
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(3)
            time.sleep(2)
            tag_a = driver.find_elements_by_xpath('//a[@class="sqdOP yWX7d     _8A5w5   ZIAjV "]')
            profile_hrefs = [elem.get_attribute('href') for elem in tag_a]
            for i in profile_hrefs:
                if i not in list_no_repetition:
                    list_no_repetition.append(i)
            print(str(len(profile_hrefs)))
            print(profile_hrefs)
            print(list_no_repetition)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Olha que paid'égua: encontrei {len(list_no_repetition)} fotos pra curtir")
            time.sleep(3)
            for profile in list_no_repetition:
                driver.get(profile)
                time.sleep(3)
                driver.find_element_by_xpath('//div[@class="_9AhH0"]') \
                    .click()
                time.sleep(2)
                button = driver.find_element_by_xpath('//span[@class="fr66n"]')
                button.click()
                count_like+=1
                time.sleep(3)
        except Exception as e:
            print(e)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Erro: {e}")
        finally:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Acabei de curtir {count_like} fotos do seu feed. Deseja fazer mais alguma coisa?\n\n" \
                                          "Digite 1 para seguir, 2 para curtir e 3 para comentar")
            return OPTIONS
    elif response_option_follow == '2':
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Você deseja curtir fotos de qual hashtag? ")
        return HASH_CURTIR

    elif response_option_follow == 'SAIR':
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Pena que você já vai.\n\n Se precisar de mim é só chamar")
        data.clear()
        return ConversationHandler.END
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Desculpe, não entendi. Vou repetir as opções:\n\n"
                                      "Digite 1 para curtir fotos do feed\n" \
                                      "Digite 2 para curtir fotos de alguma hashtag\n\n"
                                      "Para cancelar digite sair")
        return OPTIONS_LIKE


def curte_fotos(update, context):
    response_hashtag_curtir = (update.message.text).upper()
    if response_hashtag_curtir == "SIM" or response_hashtag_curtir == "S" or response_hashtag_curtir == "PODEMOS":
        context.bot.send_message(chat_id=update.effective_chat.id, text="Então vamos começar!")
        time.sleep(2)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        #driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        driver = webdriver.Chrome(executable_path="/home/tom/PycharmProjects/Bot/mastermind/chromedriver")
        driver.get("https://instagram.com")
        time.sleep(2)
        list_no_repetition = []
        count_like = 0
        try:
            driver.find_element_by_xpath("//input[@name=\"username\"]") \
                .send_keys(data[0])
            driver.find_element_by_xpath("//input[@name=\"password\"]") \
                .send_keys(data[1])
            driver.find_element_by_xpath('//button[@type="submit"]') \
                .click()
            time.sleep(3)
        except Exception as erro:
            print(erro)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Deu ruim: Eu acho que você pode ter errado seus dados ou sua internet está instável\n\n" \
                                          f"Bora de novo?")
            return BEGIN
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"Eu tô dando uma olhada aqui nna hashtag {data[2]} em busca das melhores fotos pra curtir...")
        try:
            driver.get("https://www.instagram.com/explore/tags/" + data[2] + "/")
            time.sleep(3)
            for c in range(4):
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(3)
            hrefs = driver.find_elements_by_tag_name("a")
            pic_hrefs = [elem.get_attribute("href") for elem in hrefs]
            for i in pic_hrefs:
                if i not in list_no_repetition:
                    list_no_repetition.append(i)
            print(str(len(pic_hrefs)))
            print(pic_hrefs)
            print(list_no_repetition)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Olha que paid'égua: encontrei {len(list_no_repetition)} fotos pra curtir na hashtag {data[2]}")
            time.sleep(3)
            for pic_href in list_no_repetition:
                driver.get(pic_href)
                button = driver.find_element_by_xpath('//span[@class="fr66n"]')
                button.click()
                count_like+=1
                time.sleep(3)
        except Exception as e:
            print(e)
            time.sleep(5)
        finally:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Acabei de curtir {count_like} fotos da hashtag #{data[2]}. Deseja fazer mais alguma coisa?\n\n" \
                                          "Digite 1 para seguir, 2 para curtir e 3 para comentar")
            return OPTIONS
    if response_hashtag_curtir == "NÃO" or response_hashtag_curtir == "N":
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Pena que você já vai.\n\n Se precisar de min é só chamar")
        data.clear()
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Desculpe, não entendi. Vou repetir as opções:\n\n"\
                                      "Digite 1 para curtir fotos do feed\n" \
                                      "Digite 2 para curtir fotos de alguma hashtag\n\n"
                                      "Para cancelar digite sair")
        return OPTIONS_LIKE


def hashtag_curtir(user_hashtag_curtir):
    answer_hashtag_curtir = "Você deseja pesquisar por: #"+ user_hashtag_curtir + ".\n\n Podemos começar?"
    data.insert(2, user_hashtag_curtir)
    print(data[2])
    return answer_hashtag_curtir

def reply_hashtag_curtir(update, context):
    user_hashtag_curtir = update.message.text
    update.message.reply_text(hashtag_curtir(user_hashtag_curtir))
    return CURTE_FOTOS

def options_follow(update, context):
    response_option_follow = (update.message.text).upper()
    if response_option_follow == "1":
        context.bot.send_message(chat_id=update.effective_chat.id, text="Então vamo arrochaaaar...")
        time.sleep(2)
        count_follow = 0
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        #driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        driver = webdriver.Chrome(executable_path="/home/tom/PycharmProjects/Bot/mastermind/chromedriver")
        driver.get("https://instagram.com")
        time.sleep(2)
        try:
            driver.find_element_by_xpath("//input[@name=\"username\"]") \
                .send_keys(data[0])
            driver.find_element_by_xpath("//input[@name=\"password\"]") \
                .send_keys(data[1])
            driver.find_element_by_xpath('//button[@type="submit"]') \
                .click()
            time.sleep(3)
        except Exception as erro:
            print(erro)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Deu ruim: Dá uma olhada se seus dados estão corretos ou se a sua internet ta funcionando\n\n"\
                                          f"Bora começar de novo?")
            return BEGIN
        try:
            driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]") \
                .click()
            time.sleep(3)
            driver.get("https://www.instagram.com/explore/people/suggested/")
            time.sleep(2)
            for i in range(int(data[2])):
                driver.find_element_by_xpath('//button[text()="Follow"]') \
                    .click()
                count_follow+=1
                time.sleep(2)
            driver.refresh()
        except Exception as e:
            print(e)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Erro: {e.__class__}")
        finally:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Acabei de seguir {count_follow} pessoas pra você. Deseja fazer mais alguma coisa?\n\n" \
                                          "Digite 1 para seguir, 2 para curtir e 3 para comentar")
            return OPTIONS
    elif response_option_follow == '2':
        context.bot.send_message(chat_id=update.effective_chat.id, text="Qual perfil você deseja seguir e extrair seguidores?")
        return FOLLOW_PROFILE
    elif response_option_follow == '3':
        context.bot.send_message(chat_id=update.effective_chat.id, text="De qual perfil você deseja extrair seguidores?")
        return FOLLOW_PROFILE2
    elif response_option_follow == 'SAIR':
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Pena que você já vai.\n\n Se precisar de min é só chamar")
        return ConversationHandler.END
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Desculpe, não entendi. Vou repetir as opções:\n\n"
                                    "Digite 1 para seguir por sugeridos\n" \
                                    "Digite 2 para seguir por perfil e sugeridos \n" \
                                    "Digite 3 para seguir por perfil\n" \
                                    "Digite 4 para seguir por localização\n\n"
                                    "Para cancelar digite sair")
        #data.clear()
        return OPTIONS_FOLLOW
def follow_profile(user_follow_profile):
    answer_follow_profile = "Você deseja extrair seguidores do perfil: @"+ user_follow_profile + ".\n\n Podemos começar?"
    data.insert(3, user_follow_profile)
    print(data[3])
    return answer_follow_profile

def reply_follow_profile(update, context):
    user_follow_profile = update.message.text
    update.message.reply_text(follow_profile(user_follow_profile))
    return FOLLOW_BY_PROFILE

def follow_by_profile(update, context):
    response_follow_profile = (update.message.text).upper()
    if response_follow_profile == "SIM" or response_follow_profile == "S":
        context.bot.send_message(chat_id=update.effective_chat.id, text="Vamo arrochaaaar!")
        time.sleep(2)
        count_follow = 0
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        #driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        driver = webdriver.Chrome(executable_path="/home/tom/PycharmProjects/Bot/mastermind/chromedriver")
        driver.get("https://instagram.com")
        time.sleep(2)
        try:
            driver.find_element_by_xpath("//input[@name=\"username\"]") \
                .send_keys(data[0])
            driver.find_element_by_xpath("//input[@name=\"password\"]") \
                .send_keys(data[1])
            driver.find_element_by_xpath('//button[@type="submit"]') \
                .click()
            time.sleep(3)
        except Exception as erro:
            print(erro)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Deu ruim: Será que você digitou seus dados errados?\n\n"\
                                          f"Bora começar novamente?")
            return BEGIN
        try:
            driver.get("https://www.instagram.com/"+ data[3] +"/followers/?hl=pt-br")
            time.sleep(3)
            for i in range(int(data[2])):
                driver.find_element_by_xpath('//button[text()="Follow"]') \
                    .click()
                count_follow+=1
                time.sleep(2)
            driver.refresh()
        except Exception as e:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Erro: {e.__class__}")
            print(e)
        finally:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Acabei de seguir {count_follow} pessoas pra você. Deseja fazer mais alguma coisa?\n\n" \
                                          "Digite 1 para seguir, 2 para curtir e 3 para comentar")
            return OPTIONS
    elif response_follow_profile == "NÃO" or response_follow_profile == "N":
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Até logo!")
        data.clear()
        return ConversationHandler.END
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Desculpe, não entendi. Vou repetir as opções:\n\n"\
                                      "Digite 1 para seguir por sugeridos\n"\
                                      "Digite 2 para seguir por perfil e sugeridos \n" \
                                      "Digite 3 para seguir por perfil\n" \
                                      "Digite 4 para seguir por localização\n\n"\
                                      "Para cancelar digite sair")
        return OPTIONS_FOLLOW

def reply_follow_profile2(update, context):
    user_follow_profile = update.message.text
    update.message.reply_text(follow_profile(user_follow_profile))
    return FOLLOW_BY_PROFILE2

def follow_by_profile2(update, context):
    response_follow_profile = (update.message.text).upper()
    if response_follow_profile == "SIM" or response_follow_profile == "S":
        context.bot.send_message(chat_id=update.effective_chat.id, text="Vamo arrochaaaar!")
        time.sleep(2)
        count_follow = 0
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        #driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        driver = webdriver.Chrome(executable_path="/home/tom/PycharmProjects/Bot/mastermind/chromedriver")
        driver.get("https://instagram.com")
        time.sleep(2)
        try:
            driver.find_element_by_xpath("//input[@name=\"username\"]") \
                .send_keys(data[0])
            driver.find_element_by_xpath("//input[@name=\"password\"]") \
                .send_keys(data[1])
            driver.find_element_by_xpath('//button[@type="submit"]') \
                .click()
            time.sleep(3)
        except Exception as e:
            print(e)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Deu ruim: Verifica pra mim, por favor, se ta tudo ok com seus dados...\n\n" \
                                          f"Bora começar novamente?")
            return BEGIN
        try:
            driver.get("https://www.instagram.com/"+ data[3] +"/")
            time.sleep(3)
            element = driver.find_element_by_xpath('//a[@href="/'+ data[3] +'/followers/"]')
            element.click()
            time.sleep(2)
            for i in range(int(data[2])):
                driver.find_element_by_xpath('//button[text()="Follow"]') \
                    .click()
                count_follow+=1
                time.sleep(2)
            driver.refresh()
        except Exception as e:
            print(e)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Erro: {e.__class__}")
        finally:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Acabei de seguir {count_follow} pessoas pra você. Deseja fazer mais alguma coisa?\n\n" \
                                          "Digite 1 para seguir, 2 para curtir e 3 para comentar")
            return OPTIONS
    elif response_follow_profile == "NÃO" or response_follow_profile == "N":
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Até logo!")
        data.clear()
        return ConversationHandler.END
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Desculpe, não entendi. Vou repetir as opções:\n\n"\
                                      "Digite 1 para seguir por sugeridos\n"\
                                      "Digite 2 para seguir por perfil e sugeridos \n" \
                                      "Digite 3 para seguir por perfil\n" \
                                      "Digite 4 para seguir por localização\n\n"\
                                      "Para cancelar digite sair")
        return OPTIONS_FOLLOW

def cancel(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Pena que você já vai. \n\nSe precisar de mim é só chamar!!!")
    return ConversationHandler.END
def main():
    #TOKEN="1368978547:AAEoYdgxdm586q7tcF1xQT3OpL3SBZBNLT00"
    #updater = Updater(token=TOKEN, use_context=True)
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
    fallbacks=[CommandHandler('start', cancel)]
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
main()
