# -*- coding: utf-8 -*-

import pandas as pd
import re
import pymorphy2
from collections import Counter
from mystopwords import stopWords

morph = pymorphy2.MorphAnalyzer()
stop_words = stopWords()

def normalize(text):
    global stop_words
    words = {}
    fine_text = re.sub("[^а-яА-ЯЁё]"," ", text)    
    try:
        all_words = fine_text.lower().split()
    except IndexError:
        all_words = ''
    for word in all_words:
        p = morph.parse(word)[0]
        if word not in stop_words and  p.normal_form not in stop_words:
            words[word] = p.normal_form
    return(words)

texts = []
table = []
for i in range(14):
    name = 'bns_ru\\comments'+str(i)+'.csv'
    delimiter=';'
    try:
        table += [pd.read_csv(name, header=0, \
                    delimiter=delimiter, quoting=3)]
    except FileNotFoundError:
        continue
for frame in table:
    for i in range(len(frame)):
        texts.append(frame['text'][i])

words = []
lemmas = []
for text in texts:
    if type(text) == str:
        words += text.split()
        norm_text = normalize(text)
        lemmas += (list(norm_text.values()))
    
common_words = Counter(words).most_common()
common_lemmas = Counter(words).most_common()

for word in common_words:
    if word[0] in stop_words:
        common_words.remove(word)