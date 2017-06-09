# -*- coding: utf-8 -*-
#import math
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.externals import joblib
import time
from nltk import ngrams
import string
import re
from mystopwords import stopWords

train = pd.read_csv(r'train.csv', header=0, \
                    delimiter='\t', quoting=3)
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

def comment_to_words(raw_comment):
    raw_comment = str(raw_comment).replace('_','')
    words = raw_comment.split()
    #stops = set(stopwords.words('russian'))
    #stops = list(stops)
    #stops += stopWords()
    #meaningful_words = [w for w in words if not w in stops]
    meaningful_words = " ".join(words )
    ngrams = ngramize(meaningful_words,2)
    fine_ngrams = []
    for ngram in ngrams:
        fine_ngrams.append(ngram[0]+'_'+ngram[1])
    if len(fine_ngrams) > 0:
        return( " ".join( fine_ngrams ))
    else:
        return meaningful_words
    
print('Cleaning and parsing the training set comments')
clean_train_comments = []
num_reviews = train['text'].size
for i in range(num_reviews):
    clean_train_comments.append(comment_to_words(train['text'][i]))

print('Creating the bag of words...') 
  
vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 5000) 
#joblib.dump(vectorizer.vocabulary, "vectorizer.pkl") 
#vocabulary_to_load =joblib.load("vectorizer.pkl")
#loaded_vectorizer = CountVectorizer(vocabulary=vocabulary_to_load)
#loaded_vectorizer._validate_vocabulary()

train_data_features = vectorizer.fit_transform(clean_train_comments)
train_data_features = train_data_features.toarray()

vocab = vectorizer.get_feature_names()
dist = np.sum(train_data_features, axis=0)

print('Training the random forest...')
forest = RandomForestClassifier(n_estimators=5000, criterion='entropy', 
                             max_leaf_nodes=None, bootstrap=True, oob_score=False, 
                             n_jobs=1, random_state=None, verbose=0)

print('Fitting forest')
forest = forest.fit(train_data_features, train['mark'])
print('Save model')
joblib.dump(forest, r'C:\Users\Ania\Desktop\forest + 0.pkl') 
#forest = joblib.load('forest.pkl')
test = pd.read_csv(r"test.csv", header=0, delimiter="\t", \
                   quoting=3 )
num_comments = test["text"].size
clean_test_comments = []
for i in range(num_comments):
    clean_comment = comment_to_words(test['text'][i])
    clean_test_comments.append(clean_comment)

test_data_features = vectorizer.transform(clean_test_comments)
test_data_features = test_data_features.toarray()

time.sleep(3)
result1 = forest.predict(test_data_features)
time.sleep(3)

output = pd.DataFrame( data={"text":test['text'],\
                             "check_sentiment":test["check_sentiment"],\
                             "sentiment":result1} )

output.to_csv(r"result.csv")
