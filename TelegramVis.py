
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, InlineQueryHandler, RegexHandler, CallbackQueryHandler, CallbackContext)
import requests
import re

import logging
import VisuData


import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]


def detect_intent_texts(text):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    # bothandle
    project_id = "support-brhy"
    session_id = "test"
    language_code = "ru"

    import dialogflow_v2 as dialogflow
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    # for text in texts:
    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(
        response.query_result.fulfillment_text))
    return response.query_result.fulfillment_text


"""
headers = {'user-agent': 'your-own-user-agent/0.0.1'}
cookies = {'visit-month': 'February'}
query = {'q': 'Forest', 'order': 'popular', 'min_width': '800', 'min_height': '600'}

req = requests.get(url, headers=headers, cookies=cookies)
,params=query
 ,params=query

"""


def get_dog_url(text):
    headers = {'x-api-key': API_Key}
    #contents = requests.get('https://api.thedogapi.com/v1/images/search',headers=headers).json()
    # print(contents[0])
    if "hat" in text:
        query = {'category_ids': '1'}
    if "funny" in text or "silly" in text:
        query = {'category_ids': '3'}
    else:
        query = None
    headers = {'x-api-key': API_Key}
    contents = requests.get(
        'https://api.thedogapi.com/v1/images/search', headers=headers, params=query).json()
    # print(contents)
    url = contents[0]['url']
    return url


def get_cat_url(text):
    headers = {'x-api-key': API_Key}
    #contents = requests.get('http://api.thecatapi.com/v1/categories',headers=headers).json()
    # print(contents[0])
    query = None
    if "hat" in text:
        print("haT is here")
        query = {'category_ids': '1'}
    elif "funny" in text or "silly" in text:
        query = {'category_ids': '3'}
    elif "space" in text:
        query = {'category_ids': '2'}
    elif "sungla" in text:
        query = {'category_ids': '4'}
    print(query)
    headers = {'x-api-key': API_Key}
    contents = requests.get(
        'http://api.thecatapi.com/v1/images/search', headers=headers, params=query).json()
    # print(contents)
    url = contents[0]['url']
    return url


def bop(bot: Update, context: CallbackContext):
    url = get_dog_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)


def help_command(update, context):
    update.message.reply_text("Use /start to test this bot.")
    # print(update.message.text.lower())
    #context.bot.send_message(chat_id=chat_id,text="Hey "+ str(update.message.from_user.username)+", Cat or Dog?")


def start_callback(update, context):
    print(dir(update.message))
    # print(dir(context.bot))
    chat_id = update.message.chat_id
    #user_says = " ".join(context.args)
    #update.message.reply_text("You said: " + user_says)
    if ("help" in update.message.text.lower()):
        # print(context.message.from_user.username)
        context.bot.send_message(chat_id=chat_id, text="Hey " + str(update.message.from_user.username) +
                                 ", if you are trying to use comands try / befor word, like this /help")
        help_command(update, context)
    elif ("dog" in update.message.text.lower()) and ("cat" in update.message.text.lower()):
        url = "https://i.ytimg.com/vi/54Afdxd6sUQ/maxresdefault.jpg"
        context.bot.send_photo(chat_id=chat_id, photo=url)
    elif "dog" in update.message.text.lower():
        url = get_dog_url(update.message.text.lower())
        context.bot.send_photo(chat_id=chat_id, photo=url)
    elif "cat" in update.message.text.lower():
        url = get_cat_url(update.message.text.lower())
        context.bot.send_photo(chat_id=chat_id, photo=url)
    elif "my name is" in update.message.text.lower():
        update.message.text.lower()
        #clean = re.compile('(?<=\bmy name is\s)(\w+)')
        name = re.findall(r'(?<=\bmy name is\s)(\w+)',
                          update.message.text.lower())[0]
        context.bot.send_message(
            chat_id=chat_id, text="Your name is "+name.capitalize())
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO personality (Name) VALUES (%s)", ([name]))
            conn.commit()
        finally:
            conn.close()
            cursor.close()
    else:
        context.bot.send_message(
            chat_id=chat_id, text=detect_intent_texts(update.message.text.lower()))


def start_callback2(update: Update, context: CallbackContext):
    print(update.message.text.lower())


def button(update: Update, context: CallbackContext):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    if (query.data == '3'):
        ST(Update, CallbackContext)
    else:
        query.edit_message_text(text="Selected option: {}".format(query.data))


def ST(update: Update, context: CallbackContext):
    print("dsfsdf")
    keyboard = [InlineKeyboardButton(
        "Cat", callback_data='1'), InlineKeyboardButton("Dog", callback_data='2')]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def start(update, context):
    update.message.reply_text(VisuData.main_menu_message(),
                              reply_markup=VisuData.main_menu_keyboard())


def main_menu(update, context):
    query = update.callback_query
    query.edit_message_text(text=VisuData.main_menu_message(
    ), reply_markup=VisuData.main_menu_keyboard())


def first_menu(update, context):
    query = update.callback_query
    query.edit_message_text(text=VisuData.first_menu_message(
    ), reply_markup=VisuData.first_menu_keyboard())


def main():
    updater = Updater(
        KEY, use_context=True)
    dp = updater.dispatche

    dp.add_handler(RegexHandler('[\s\S]*', start_callback))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
