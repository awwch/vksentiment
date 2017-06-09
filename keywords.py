# -*- coding: utf-8 -*-
import pandas as pd
import math
from collections import Counter
import pymorphy2
from mystopwords import stopWords

stop_words = stopWords()
morph = pymorphy2.MorphAnalyzer()
def tfIdf(word,text,corpus):
    c = text.count(word)
    tf = c/len(text)
    idf = math.log10(len(corpus)/sum([1 for i in corpus if word in i]))#i[1]]))
    return tf*idf
   
def tfIdfData(corpus): 
    mean = []
    tfidf = []
    for text in corpus:
        for word in text:
            mean.append(tfIdf(word,text,corpus))
            print(tfIdf(word,text,corpus))
    mean = sum(mean)/len(mean)
    for text in corpus:
        text_metrix = {}
        for word in text:
            if tfIdf(word,text,corpus) > mean:
                text_metrix[word] = tfIdf(word,text,corpus)
        tfidf.append((text,text_metrix))
        print(text,text_metrix)
    return tfidf

def kWords(tfidf): 
    global stop_words,morph
    tf_wordlist = []
    words=[]
    freq = []
    for post in tfidf:
        try:
            tf_wordlist.append((post[0],list(post[1].keys())))
        except:
            continue
    for i in tf_wordlist:
        for j in tf_wordlist:
            if i[1] != j[1]:
                if list(set(i[1]) & set(j[1])) != []:
                    result = (i[0],j[0],list(set(i[1]) & set(j[1])))
                    if result not in words:
                        words.append(result)
    for line in words:
        freq.extend(line[2])
    freq = Counter(freq).most_common()
    for word in freq:
        p = morph.parse(word[0])[0]
        gram_info = str(p.tag)
        if 'NOUN' not in gram_info or word in stop_words:
            freq.remove(word)
    return freq

table = pd.read_csv(r'posts.csv', header=0, \
                    delimiter=',', quoting=3)

corpus = []
for i in range(len(table)):
    corpus.append(table['text'][i])
    
fine_corpus = []
for element in corpus:
    element = str(element)
    fine_corpus.append(element.split())
    
tfidf = tfIdfData(fine_corpus)
kwords = kWords(tfidf)