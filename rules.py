# -*- coding: utf-8 -*-
import re
from time import sleep
import pandas as pd
from string import punctuation

n = '12' 
name = r'result.csv'
table = pd.read_csv(name, header=0, \
                    delimiter=',', quoting=3)

p = list(punctuation)
with open('pos_list.txt','r',encoding = 'utf-8') as f:
    abs_pos_dict = f.readlines()

with open('neg_list.txt','r',encoding = 'utf-8') as f:
    abs_neg_dict = f.readlines()

ngrams_dict = '''
К сожалению
вынуждены продлить профилактику
не могу зайти
загрузке страницы произошла ошибка
ФИКС ДЕСТРОВ
зайти не могу
ничего не происходит
что делать если
игра не запускается
что за фигня
что за ошибка
произошла ошибка
у меня ошибка
ЗАПУСКАЕМ ГУСЯРАБОТЯГИ
ЗАПУСКАЕМ ГУСЯРАБОТЯГУ
испорченное настроение
забить на ивент
убогая иннова
'''.lower().split('\n')

def abs_sent(comment,sentiment):
    global abs_pos_dict,abs_neg_dict,ngrams_dict
    text = comment
    fine_comment = text.lower()
    for punct in p:
        fine_comment = fine_comment.replace(punct,' ')

    g = re.search('ггг+',fine_comment)
    if g != None:
        abs_neg_dict.append(g.group())
        
    words = fine_comment.split(' ')
    
    for word in abs_pos_dict:
        if word != '':
            if word in words and 'не' not in words and sentiment != 3:
                text = str(comment)+',POS'             
            elif word in words and 'не' in words and sentiment != 3:
                if words.index('не') != words.index(word)-1:
                    text = str(comment)+',POS'
         
    for word in abs_neg_dict:
        if word != '':
            if word in words and 'не' not in words and sentiment != 1:
                text = str(text)+',NEG'
            elif word in words and 'не' in words and sentiment != 1:
                if words.index('не') != words.index(word)-1:
                    text = str(text)+',NEG'
            
    for ngram in ngrams_dict:
        if ngram != '' and ngram in fine_comment and sentiment != 1:
            text = str(text) + ',NEG'
            
    return text
            
def invent(comment,sentiment):
    pos_inventors = '''
виноват
виноваты
виснет
выкидывает
выкинуло
вылетает
вылетаю
вылетел
вылетела
зависает
лагает
мешает
придется
придётся
проблема
проседает
фризит
'''
    neg_inventors = '''
везет
дали
дают
доступна
запускается
запустят
заходит
интересный
исправили
легче
лучше
люблю
могу
может
надеюсь
нравится
нравятся
ответили
повезло
позволяет
получается
помог
помогает
помогло
поможет
понравилась
понравились
понравился
починили
починят
пускает
работает
работают
радует
удалось
успею
устраивает
'''.lower().split('\n')
    text = comment
    fine_comment = text.lower()
    for punct in p:
        fine_comment = fine_comment.replace(punct,' ')
        
    words = fine_comment.split(' ')
    
    for word in words:
        if word != '':
            if word in pos_inventors and 'не' in words and words.index('не') == words.index(word)-1 and sentiment != 3:
                text = str(comment)+',POS'
            elif word in neg_inventors and 'не' in words and words.index('не') == words.index(word)-1 and sentiment != 1:
                text = str(comment)+',NEG'
    return text

columns = 'check_sentiment,sentiment,text,rule\n'
with open(r'result rules.csv'
          ,'a',encoding = 'utf-8') as f:
    f.write(columns)
    for j in range(len(table)):
        line = str(table['check_sentiment'][j]) + ',' + str(table['sentiment'][j]) + ','                
        comment = str(table['text'][j])
        sentiment = table['sentiment'][j]
        new_comment = abs_sent(comment,sentiment)
        if new_comment != None:
            new_comment = invent(new_comment,sentiment)
        if new_comment == None or sentiment == 1:
            new_comment = str(table['text'][j]) + ',no rule'
        f.write(line+str(new_comment)+'\n')