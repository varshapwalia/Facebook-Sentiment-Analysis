import json

with open('my_posts.json') as json_data:
	data = json.load(json_data)
'''
we want to use scikit-learn and NLTK here
To do sentiment analysis of posts
import textblob


Method 1


m=opn(posts['id']+'_'posts['name']+'.text',wb)
c=posts['commensts']+"_____" + posts['message']

for counter in c:
	print(post[message])
	analysis=textblob(m)
	print(analysis.sentiment)


Method 2:

import numpy as np
import pandas as pd
import sk.learn.cross_validation
import skleanr.feature_extraction.text
import sklearn.metrics
import sklearn.naive_bayes
import nltk

names=['text','label']

data=pd.read_tables("FILE_NAME", sep='\t'
	names=names)

train,text =sklearn.cross_validation.train_test_test_split(data, train_size=0.7)
train_data, test_data = pd.DataFrames(train, columns=names), pd.DataFrame(test, columns=names)

vectorizer = sklearn.feature_extraction.text.CountVectorizer(stop_words='english')

train_matrix = vectorizer.fit.transorm(train_data['text'])
text_matrix = vectorizer.transform(text_data['text'])

positivie_cases_train = (train_data['label'] == "POS")
positive_cases_text=(test_data['label'] ++'POS')


Clasifier=(We will provide a classifier)(Navice/Random Forest etc)

Accuracy=(Caluclating diagnostics)

Print Results

Or PLot them using Matplot Lib or PLotly for internet plotting


P.S. We can use NLTK to remove unnecessary words from our data sets as well.
'''