# -*- coding: utf-8 -*-
import telebot
from telebot import types
from config import token, start_message
from BotApi import Dictionary

bot = telebot.TeleBot(token)
dictionary = Dictionary()


@bot.message_handler(commands = ['start', 'help'])
def send_help_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, start_message, parse_mode='markdown')

@bot.message_handler(commands = ['oxford', 'wiki', 'cyclo','inter'], content_types=['text'])
def default_message_handler(message):
    if message.new_chat_member or not message.text:
        return
    query = message.text.replace('@Meanings_of_words_Bot', '')
    reply = make_reply(query)
    if reply != '':
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, reply, parse_mode='markdown')

def make_reply(query):
    reply_message = ''
    query = query.split()
    if len(query) > 1:
        if query[0] in ['/oxford', '/wiki', '/cyclo','/inter']:
            if query[0] == '/oxford':
                word = ' '.join(query[1::])
                message, word = dictionary.GetDefinitionOxfDic(word)
                reply_message = '*' +  word.swapcase() + '*\n\n'
                reply_message += message + '\n'
            if query[0] == '/wiki':
                word = ' '.join(query[1::])
                print(word)
                message = dictionary.GetDefinitionWikiDic(word)
                reply_message = '*' + word.swapcase() + '*\n\n'
                reply_message += message + '\n'
            if query[0] == '/cyclo':
                word = ' '.join(query[1::])
                message = dictionary.GetDefinitionCycDic(word)
                reply_message = '*' + word.swapcase() + '*\n\n'
                reply_message += message + '\n'
            if query[0] == '/inter':
                word = ' '.join(query[1::])
                message = dictionary.GetDefinitionInterDic(word)
                reply_message = '*' + word.swapcase() + '*\n\n'
                reply_message += message + '\n'
        return reply_message



if __name__ == '__main__':

   bot.polling(none_stop=True)


