# -*- coding: utf-8 -*-

import re
#import math
import pymorphy2
from collections import Counter
import gensim
from gensim import corpora
#import string
from mystopwords import stopWords

morph = pymorphy2.MorphAnalyzer()

stop_words = stopWords()        

def normalize(text):
    global stop_words
    _id = text[0]
    words = {}
    fine_text = re.sub("[^а-яА-ЯЁё]"," ", text[1])    
    try:
        all_words = fine_text.lower().split()
    except IndexError:
        all_words = ''
    for word in all_words:
        p = morph.parse(word)[0]
        if word not in stop_words and  p.normal_form not in stop_words:
            words[word] = p.normal_form
    post = (_id,words)
    return(post)

def getCorpus(f):
    start_time = 1464739201
    finish_time = 1481846401
    texts = []
    posts = [] 
    corpus = []
    fine_texts = []
    with open(f,'r',encoding = 'utf-8') as f:
        lines = f.readlines()
    lines.remove(lines[0])    
    for line in lines:
        line = line.split(',')
        if int(line[1]) >= start_time and int(line[1]) <= finish_time:
            if line[-2] != '':
                texts.append([line[0],line[-2]+'\\\\'+line[-1]])
            else:
                texts.append([line[0],line[-1]])
                fine_texts.append([line[0],line[-1].split()])
    for text in texts:
        posts.append(normalize(text))
    for post in posts:
        corpus.append((post[0],list(post[1].values())))
    return (fine_texts,corpus)

texts,corpus = getCorpus('posts.csv')
all_words = []
for post in corpus:
    all_words = all_words + post[1] 
print('Corpus created')
    
common_words = Counter(all_words).most_common()
for word in common_words:
    p = morph.parse(word[0])[0]
    gram_info = str(p.tag)
    if 'NOUN' not in gram_info or word[0] in stop_words or p.normal_form in stop_words:
        common_words.remove(word)
print('Common words: ',common_words[:50])

fine_corpus = []
for doc in corpus:
    fine_doc = doc[1]
    for word in fine_doc:
        if word not in common_words:
            fine_doc.remove(word)
    fine_doc.insert(0,doc[0])
    fine_corpus.append(fine_doc)

dictionary = corpora.Dictionary(fine_corpus)
print('Dictionary created')

doc_term_matrix= []
for post in fine_corpus:
    doc_term_matrix.append(dictionary.doc2bow(post))
print('Matrix created')
print('Learning model...')
Lda = gensim.models.ldamodel.LdaModel
ldamodel = Lda(doc_term_matrix, num_topics=10, id2word = dictionary, passes=100)

print(ldamodel.print_topics(num_topics=10, num_words=5))
print(ldamodel.top_topics(doc_term_matrix,num_words=20))