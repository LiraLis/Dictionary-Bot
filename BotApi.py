import requests
import json
from config import app_id, app_key, word_key


class Dictionary(object):

    def GetDefinitionOxfDic(self, word):
        word_id = word
        url_1 = 'Oxford_Url_1' + word_id.lower()
        json_data = []
        r = requests.get(url_1, headers={'app_id': app_id, 'app_key': app_key})
        if r.status_code != 404:
            json_data.append(json.loads(r.text))
            if len(json_data[0]["results"][0]["lexicalEntries"]) > 1:
                word_id = str(json_data[0]["results"][0]["lexicalEntries"][1]["inflectionOf"][0]["id"])
            else:
                word_id = str(json_data[0]["results"][0]["lexicalEntries"][0]["inflectionOf"][0]["id"])
            url = 'Oxford_Url' + word_id.lower()
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
            str_2 += '\nChosen dictionary: ' + '*Oxford Dictionary of English*'
            return str_2, word_id
        else:
            str_1 = 'No exact matches found for "' + word + '"\n'
            str_1 += '\nChosen dictionary: ' + '*Oxford Dictionary of English*'
            return str_1, word_id

    def GetDefinitionWikiDic(self, word_id):
        w_dict = 'wiktionary'
        word_url = 'http://api.wordnik.com:80/v4/word.json/' + word_id.lower() + '/definitions?limit=15&includeRelated=false&' \
                                                                                 'sourceDictionaries=' + w_dict + \
                   '&useCanonical=false&includeTags=false&api_key=' + word_key
        json_data = []
        wordData = []
        r = requests.get(word_url)
        json_data.append(json.loads(r.text))
        if r.status_code != 404 and len(json_data) > 0:
            str_2 = ''
            k = 0
            while True:
                if k < len(json_data[0]):
                    str_1 = str(json_data[0][k]['text'])
                    str_1 = '>> ' + str_1 + '\n'
                    wordData.append(str_1)
                    k += 1
                else:
                    break
            str_2 += '\n'.join(wordData)
            str_2 += '\nChosen dictionary: ' + '*Wiktionary*'
            return str_2
        else:
            str_1 = 'No exact matches found for "' + word_id + '"\n'
            str_1 += '\nChosen dictionary: ' + '*Wiktionary*'
            return str_1

    def GetDefinitionInterDic(self, word_id):
        w_dict = 'gcide'
        word_url = 'Dictionary_of_English_url' + word_id.lower() +  w_dict + word_key
        json_data = []
        wordData = []
        r = requests.get(word_url)
        json_data.append(json.loads(r.text))
        if r.status_code != 404 and len(json_data[0]) > 0:
            json_data.append(json.loads(r.text))
            str_2 = ''
            k = 0
            while True:
                if k < len(json_data[0]):
                    str_1 = str(json_data[0][k]['text'])
                    str_1 = '>> ' + str_1 + '\n'
                    wordData.append(str_1)
                    k += 1
                else:
                    break
            str_2 += '\n'.join(wordData)
            str_2 += '\nChosen dictionary: ' + '*The Collaborative International Dictionary of English*'
            return str_2
        else:
            str_1 = 'No exact matches found for "' + word_id + '"\n'
            str_1 += '\nChosen dictionary: ' + '*The Collaborative International Dictionary of English*'
            return str_1

    def GetDefinitionCycDic(self, word_id):
        w_dict = 'century'
        word_url = 'Cyclopedia_url' + word_id.lower() + w_dict +  word_key
        json_data = []
        wordData = []
        r = requests.get(word_url)
        json_data.append(json.loads(r.text))
        if r.status_code != 404 and len(json_data[0]) > 0:
            json_data.append(json.loads(r.text))
            str_2 = ''
            k = 0
            while True:
                if k < len(json_data[0]):
                    str_1 = str(json_data[0][k]['text'])
                    str_1 = '>> ' + str_1 + '\n'
                    wordData.append(str_1)
                    k += 1
                else:
                    break
            str_2 += '\n'.join(wordData)
            str_2 += '\nChosen dictionary: ' + '*The Century Dictionary and Cyclopedia*'
            return str_2
        else:
            str_1 = 'No exact matches found for "' + word_id + '"\n'
            str_1 += '\nChosen dictionary: ' + '*The Century Dictionary and Cyclopedia*'
            return str_1


