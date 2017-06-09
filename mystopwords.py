# -*- coding: utf-8 -*-
from nltk.corpus import stopwords

def stopWords():
    stop_words = stopwords.words('russian')
    pos = ['conj', 'anum','adv', 'advpro', 'apro','intj',\
           'num', 'part', 'pr', 'spro','s.PROP','v']
    f = open('freqrnc2011.csv','r',encoding = 'utf-8')
    freq_dict= f.readlines()
    f.close()
    for line in freq_dict:
        data = line.split('\t')
        if data[1] in pos:
            stop_words.append(data[0])
    return(stop_words)