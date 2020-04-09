from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
import numpy as np

import json

def train(model, tweet):
    return model.predict(tweet)

def get_model():
    training, target = (get_training())
    text_clf = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', MultinomialNB())
    ])

    text_clf_svm = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf-svm', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42)),
    ])

    return text_clf_svm.fit(training, target)

def get_training():
    with open("bot/training.json", "r") as training_json:
        training_data = training_json.read()
        training_json.close()

    training = []
    target = []
    training_data = json.loads(training_data)
    for status in training_data:
        training.append(str(f'{status["training"]["hasUrl"]} ' +
        f'{status["training"]["user"]} ' + 
        f'{status["training"]["text"]} ' + 
        f'{status["training"]["isReply"]}'))

        target.append(status["target"])

    return training, target
