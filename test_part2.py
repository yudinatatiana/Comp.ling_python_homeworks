import re
import json
import requests
import pymorphy2
import pandas as pd
from bs4 import BeautifulSoup as BS

def preprocess(text):
    new_text = text.lower()
    new_text = re.sub('\s+', ' ', new_text) #избавилась от пробельных символов
    res = re.sub('[^А-ЯЁа-яё\-]', ' ', new_text) #избавилась от знаков препинания и чисел кроме дефиса и тире
    res = re.sub('\s+\-\s*', ' ', res) #избавилась от тире
    result = re.sub('\s+', ' ', res) #удалила лишние пробелы
    return result
    
file = open('dom.txt', encoding='utf-8-sig')
text = file.read()
file.close()

result = preprocess(text)
words = {}
mass = result.split()
for word in mass:
    if word in words:
        words[word] += 1
    else:
        words[word] = 1
        
df = pd.DataFrame.from_dict(words, orient='index', columns=['Частота'])
df.to_csv('dom.csv', encoding='cp1251')


#Вторая часть
morph = pymorphy2.MorphAnalyzer()
lemmas = []
for token in words:
    normal_form = morph.parse(token)[0].normal_form
    if normal_form.count('о') == 2 and normal_form not in lemmas:
        lemmas.append(normal_form)

file = open('dom_lemmas.txt', 'w')
for lemma in lemmas:
    file.write(str(lemma + '\n'))
file.close()

response = requests.get('http://lib.ru/POEZIQ/PESSOA/lirika.txt')
if not response:
    print('Проблема с доступом')
else:
    bs = BS(response.text, 'html.parser')
    page_text = bs.get_text()
    with open('poems.json', 'w') as file:
        json.dump(list(set(preprocess(page_text).split())), file)

