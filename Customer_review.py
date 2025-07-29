import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataset = pd.read_csv(r"E:\Datasets\Restaurant_Reviews.tsv",delimiter = '\t',quoting = 3)

import re
import nltk

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

corpus = []

for i in range(0,1000):
    review = re.sub('[^a-zA-Z]', ' ', dataset['Review'][i])
    review =review.lower()
    review = review.split()
    ps = PorterStemmer()
    review = [ps.stem(word) for word in review if not word  in set (stopwords.words('english'))]
    review = ' '.join (review)
    corpus.append(review)
    


# Creating BOW Model
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
x = cv.fit_transform(corpus).toarray()
y =  dataset.iloc[:,1].values


# Splitting dataset into Training and test set

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x,y,test_size= 0.25,random_state = 0)

from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier()
classifier.fit(x_train,y_train)

y_pred = classifier.predict(x_test)

from sklearn.metrics import confusion_matrix

cm  = confusion_matrix(y_test, y_pred)
print(cm)


from sklearn.metrics import accuracy_score
acc = accuracy_score(y_test,y_pred)

bias = classifier.score(x_train,y_train)
print(bias)

variance = classifier.score(x_test,y_test)
print(variance)





