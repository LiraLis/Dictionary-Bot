# -*- coding: utf-8 -*-
import requests
import json
import editdistance
from BotDb import GetWordDB
from config import app_id, app_key, url_ox1, url_ox,\
                   word_key,  word_url1, word_url2, word_url3


def GetLevenshtein(word):
    str = ''
    wordsList = GetWordDB(word.lower())
    for x in wordsList:
        dis = editdistance.eval(word.lower(), x)
        if dis < 2:
            str += x + ', '
    if len(str) > 0:
        str_1 = 'Did you mean: ' + '*' + str[0:len(str) - 2] + '*' + '?'
        return str_1
    else:
        str_1 = 'Your search did not match any results!'
        return str_1

class Dictionary(object):

    def GetDefinitionOxfDic(self, word):
        word_id = word
        url_1 =  url_ox1 + word_id.lower()
        json_data = []
        r = requests.get(url_1, headers={'app_id': app_id, 'app_key': app_key})
        if r.status_code != 404:
            json_data.append(json.loads(r.text))
            if len(json_data[0]["results"][0]["lexicalEntries"]) > 1:
                word_id = str(json_data[0]["results"][0]["lexicalEntries"][1]["inflectionOf"][0]["id"])
            else:
                word_id = str(json_data[0]["results"][0]["lexicalEntries"][0]["inflectionOf"][0]["id"])

            url = url_ox + word_id.lower()
            json_data = []
            r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})
            json_data.append(json.loads(r.text))
            wordData = []
            str_2 = ''
            k = 0
            while True:
                if k < len(json_data[0]["results"][0]["lexicalEntries"][0]["entries"][0]["senses"]):
                    str_1 = str(
                        json_data[0]["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][k]["definitions"])
                    str_1 = '>> ' + str_1[2:len(str_1) - 2].capitalize() + '\n'
                    wordData.append(str_1)
                    k += 1
                else:
                    break
            str_2 += '\n'.join(wordData)
            return str_2, word_id
        else:
            str_1 = GetLevenshtein(word)
            return str_1, word_id


    def GetDefinitionWikiDic(self, word_id):
        w_dict = 'wiktionary'
        word_url = word_url1 + word_id.lower() + word_url2 + w_dict + word_url3 + word_key
        json_data = []
        wordData = []
        r = requests.get(word_url)
        json_data.append(json.loads(r.text))
        if r.status_code != 404 and len(json_data[0]) > 0:
            str_2 = ''
            k = 0
            if len(json_data[0]) == 1:
                str_1 = str(json_data[0][k]['text'])
                str_1 = '>> ' + str_1 + '\n'
                wordData.append(str_1)
            else:
                while True:
                    if k < len(json_data[0]) - 1:
                        str_1 = str(json_data[0][k]['text'])
                        str_1 = '>> ' + str_1 + '\n'
                        wordData.append(str_1)
                        k += 1
                    else:
                        break
            str_2 += '\n'.join(wordData)
            return str_2
        else:
            str_1 = GetLevenshtein(word_id)
            return str_1


    def GetDefinitionInterDic(self, word_id):
        w_dict = 'gcide'
        word_url = word_url1 + word_id.lower() + word_url2 + w_dict + word_url3 + word_key
        json_data = []
        wordData = []
        r = requests.get(word_url)
        json_data.append(json.loads(r.text))
        if r.status_code != 404 and len(json_data[0]) > 0:
            str_2 = ''
            k = 0
            if len(json_data[0]) == 1:
                str_1 = str(json_data[0][k]['text'])
                str_1 = '>> ' + str_1 + '\n'
                wordData.append(str_1)
            else:
                while True:
                    if k < len(json_data[0]) - 1:
                        str_1 = str(json_data[0][k]['text'])
                        str_1 = '>> ' + str_1 + '\n'
                        wordData.append(str_1)
                        k += 1
                    else:
                        break
            str_2 += '\n'.join(wordData)
            return str_2
        else:
            str_1 = GetLevenshtein(word_id)
            return str_1

    def GetDefinitionCycDic(self, word_id):
        w_dict = 'century'
        word_url = word_url1 + word_id.lower() + word_url2 + w_dict + word_url3 + word_key
        json_data = []
        wordData = []
        r = requests.get(word_url)
        json_data.append(json.loads(r.text))
        if r.status_code != 404 and len(json_data[0]) > 0:
            json_data.append(json.loads(r.text))
            str_2 = ''
            k = 0
            if len(json_data[0]) == 1:
                str_1 = str(json_data[0][k]['text'])
                str_1 = '>> ' + str_1 + '\n'
                wordData.append(str_1)
            else:
                while True:
                    if k < len(json_data[0]) - 1:
                        str_1 = str(json_data[0][k]['text'])
                        str_1 = '>> ' + str_1 + '\n'
                        wordData.append(str_1)
                        k += 1
                    else:
                        break
            str_2 += '\n'.join(wordData)
            return str_2
        else:
            str_1 = GetLevenshtein(word_id)
            return str_1


