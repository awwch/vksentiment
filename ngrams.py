# -*- coding: utf-8 -*-
import pandas as pd
from collections import Counter
#from nltk.stem import SnowballStemmer
from nltk import ngrams
import string
import re
from mystopwords import stopWords

#st = SnowballStemmer("russian")

def ngramize(text,n):
    n_grams= []
    text = text.split()
    stop_words = stopWords()    
    for word in text:
        fine_word = word.strip(string.punctuation)
        fine_word = re.sub("[^а-яА-ЯЁё]","", fine_word)
        text.insert(text.index(word),fine_word)
        text.remove(word)
        if fine_word in stop_words or fine_word == '':
            text.remove(fine_word)
    n_grams += ngrams(text,n)
    return n_grams

table = [] 
n = 2
f = open('all '+str(n)+'-grams.txt','a',encoding = 'utf-8')         
for i in range(14):
    name = 'bns_ru\\comments'+str(i)+'.csv'
    try:
        table = pd.read_csv(name, header=0, \
                    delimiter=';', quoting=3)
        print(len(table))
        for j in range(len(table)):
            gram = ngramize(str(table['text'][j]),n)
            for g in gram:
                f.write(str(g)+'\n')
            print(len(table))
            print(j)
    except FileNotFoundError:
        continue
f.close()

with open('2.txt','r',encoding = 'utf-8') as f:
    f = f.readlines()
freq_ngrams = Counter(f).most_common()

with open('common 2-grams.txt','w',encoding = 'utf-8') as f:
    for line in freq_ngrams:
        f.write(str(line)+'\n')