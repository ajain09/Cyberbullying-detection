from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix, f1_score
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split
import pickle
import re
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split, GridSearchCV
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv(
    "https://raw.githubusercontent.com/ajain09/MachineLearning/main/Datasets/train_E6oV3lV.csv")
hate_tweet = df[df.label == 1]
normal_tweet = df[df.label == 0]


def process_tweet(tweet):
    return " ".join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])", " ", tweet.lower()).split())


df['processed_tweets'] = df['tweet'].apply(process_tweet)
cnt_non_fraud = df[df['label'] == 0]['processed_tweets'].count()
df_class_fraud = df[df['label'] == 1]
df_class_nonfraud = df[df['label'] == 0]
df_class_fraud_oversample = df_class_fraud.sample(cnt_non_fraud, replace=True)
df_oversampled = pd.concat(
    [df_class_nonfraud, df_class_fraud_oversample], axis=0)
X = df_oversampled['processed_tweets']
y = df_oversampled['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=None)

pipeline = Pipeline(steps=[('tfidf', TfidfVectorizer()),
                           ('model', SVC(C=10,
                                         gamma=0.1,
                                         kernel='sigmoid',
                                         random_state=42))])
pipeline.fit(X_train, y_train)

pickle.dump(pipeline, open('pipeline.pkl', 'wb'))
