# -*- coding: utf-8 -*-
import telebot
from telebot import types
from config import token, start_message
from BotDb import GetRating, UpdateRating, CheckUpdates
from BotApi import Dictionary
import random
from datetime import datetime
import math

bot = telebot.TeleBot(token)
dictionary = Dictionary()
globDic = ''


@bot.message_handler(commands = ['start', 'help'])
def send_help_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, start_message, parse_mode='markdown')


@bot.message_handler(commands = ['oxford', 'wiki', 'cyclo', 'inter'], content_types=['text'])
def default_message_handler(message):
    if message.new_chat_member or not message.text:
        return
    global globDic
    globDic = message.text[1::]
    sent = bot.send_message(message.chat.id, 'Enter your word, please:')
    bot.register_next_step_handler(sent, make_reply)

@bot.message_handler(commands = ['rating'])
def send_help_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    CheckUpdates()
    rateList = GetRating()
    reply_message = ('*Dictionary rating*\n\n').upper() + 'Today is: ' + datetime.strftime(datetime.now(), '%d.%m.%Y') + '\n\n'
    sum = 0
    for x in range(len(rateList)):
        if rateList[x][1] > 0:
            sum += rateList[x][1]

    for x in range(len(rateList)):
        if rateList[x][0] == 'oxford':
            dict = 'Oxford Dictionary of English - '
        if rateList[x][0] == 'wiki':
            dict = 'Wiktionary - '
        if rateList[x][0] == 'cyclo':
            dict = 'Century Dictionary and Cyclopedia - '
        if rateList[x][0] == 'inter':
            dict = 'International Dictionary of English - '
        if rateList[x][1] > 0:
            reply_message += dict +  '*' +str(math.floor((rateList[x][1] / sum) * 100)) + '%*\n'
        else:
            reply_message += dict + '*0%*\n'
    bot.send_message(message.chat.id, reply_message, parse_mode='markdown')


def make_reply(message):
    word = message.text
    mess = ''
    reply_message = ''
    if word != None and word.isalpha() and len(word) > 0:
        stat_start = random.randint(0, 2)
        if globDic == 'oxford':
            mess, word = dictionary.GetDefinitionOxfDic(word)
            reply_message = '*' + word.upper() + '*\n\n'
            reply_message += mess + '\n'
            reply_message += '\nChosen dictionary: ' + '*Oxford Dictionary of English*'
        if globDic == 'wiki':
            mess = dictionary.GetDefinitionWikiDic(word)
            reply_message = '*' + word.upper() + '*\n\n'
            reply_message += mess + '\n'
            reply_message += '\nChosen dictionary: ' + '*Wiktionary*'
        if globDic == 'cyclo':
            mess = dictionary.GetDefinitionCycDic(word)
            reply_message = '*' + word.upper() + '*\n\n'
            reply_message += mess + '\n'
            reply_message += '\nChosen dictionary: ' + '*The Century Dictionary and Cyclopedia*'
        if globDic == 'inter':
            mess = dictionary.GetDefinitionInterDic(word)
            reply_message = '*' + word.upper() + '*\n\n'
            reply_message += mess + '\n'
            reply_message += '\nChosen dictionary: ' + '*The Collaborative International Dictionary of English*'

        if reply_message != '':
            bot.send_chat_action(message.chat.id, 'typing')
            if mess[len(mess) - 1] == '?':
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in
                               ['Yes, I must have screwed up',
                                'No, the word is correct']])
                bot.send_message(message.chat.id, reply_message, reply_markup=keyboard, parse_mode='markdown')
            else:
                bot.send_message(message.chat.id, reply_message, parse_mode='markdown')
                if stat_start == 0:
                    reply_message = 'You are satisfied with the definition of the word?'
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in
                                   ['Yes', 'No', 'Skip']])
                    bot.send_message(message.chat.id, reply_message, reply_markup=keyboard, parse_mode='markdown')
    else:
        reply_message = 'Error! Please, enter the command and the word again!'
        bot.send_message(message.chat.id, reply_message, parse_mode='markdown')


@bot.callback_query_handler(func = lambda c: True)
def GetInline(c):
    if c.data == 'Yes, I must have screwed up':
        bot.send_message(chat_id = c.message.chat.id, text='Choose the command again and enter correct word, please.')
    elif  c.data == 'No, the word is correct':
        str=''
        str_2 = '\n\nP.S.\nYou can find this word in:'
        word = c.message.text.split()
        mess, word[0]= dictionary.GetDefinitionOxfDic(word[0])
        if mess[len(mess) - 1] != '?' and '!':
            str_2 += '\n*Oxford Dictionary of English* (/oxford)'
        mess = dictionary.GetDefinitionWikiDic(word[0])
        if mess[len(mess) - 1] != '?' and '!':
            str_2 += '\n*Wiktionary* (/wiki)'
        mess = dictionary.GetDefinitionCycDic(word[0])
        if mess[len(mess) - 1] != '?' and '!':
            str_2 += '\n*Cyclopedia* (/cyclo)'
        mess = dictionary.GetDefinitionInterDic(word[0])
        if mess[len(mess) - 1] != '?' and '!':
            str_2 += '\n*International Dictionary of English* (/inter)'

        if globDic == 'oxford':
            str = '*' + word[0].upper() + '*' + '\n\nYour search did not match any results!\n\nChosen dictionary: ' + '*Oxford Dictionary of English*'

        if globDic == 'wiki':
            str = '*' + word[0].upper() + '*' + '\n\nYour search did not match any results!\n\nChosen dictionary: ' + '*Wiktionary*'
        if globDic == 'cyclo':
            str = '*' + word[0].upper() + '*' + '\n\nYour search did not match any results!\n\nChosen dictionary: ' + '*The Collaborative International Dictionary of English*'
        if globDic == 'inter':
            str = '*' + word[0].upper() + '*' + '\n\nYour search did not match any results!\n\nChosen dictionary: ' + '*The Century Dictionary and Cyclopedia*'

        if str_2[len(str_2) - 1]  == ')':
            str += str_2

        bot.send_message(chat_id = c.message.chat.id, text = str, parse_mode='markdown')
    if c.data == 'Yes':
        bot.edit_message_text(chat_id = c.message.chat.id, message_id = c.message.message_id, text='Thank you for vote', parse_mode='markdown')
        UpdateRating(globDic, 1, datetime.now())
    elif c.data == 'No':
        bot.edit_message_text(chat_id = c.message.chat.id, message_id = c.message.message_id, text='Thank you for vote!', parse_mode='markdown')
        UpdateRating(globDic, -1, datetime.now())
    elif c.data == 'Skip':
        bot.edit_message_text(chat_id = c.message.chat.id, message_id = c.message.message_id, text = 'Thank you for vote!', parse_mode='markdown')


if __name__ == '__main__':
   bot.polling(none_stop=True)


