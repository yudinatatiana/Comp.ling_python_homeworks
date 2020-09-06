import re
import pandas as pd

file = open('dom.txt', encoding='utf-8-sig')
text = file.read()
file.close()
new_text = text.lower()


new_text = re.sub('\s+', ' ', new_text) #избавилась от пробельных символов
res = re.sub('[^А-ЯЁа-яё\-]', ' ', new_text) #избавилась от знаков препинания и чисел кроме дефиса и тире
res = re.sub('\s+\-\s*', ' ', res) #избавилась от тире
result = re.sub('\s+', ' ', res) #удалила лишние пробелы

words = {}
mass = result.split()
for word in mass:
    if word in words:
        words[word] += 1
    else:
        words[word] = 1

df = pd.DataFrame.from_dict(words, orient='index', columns=['Частота'])
df.to_csv('dom.csv', encoding='cp1251')