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
    "public\FinalBalancedDataset.csv")

hate_tweet = df[df.Toxicity == 1]
normal_tweet = df[df.Toxicity == 0]


def process_tweet(tweet):
    return " ".join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])", " ", tweet.lower()).split())


df['tweets'] = df['tweet'].apply(process_tweet)
cnt_non_fraud = df[df['Toxicity'] == 0]['tweets'].count()
df_class_fraud = df[df['Toxicity'] == 1]
df_class_nonfraud = df[df['Toxicity'] == 0]
df_class_fraud_oversample = df_class_fraud.sample(cnt_non_fraud, replace=True)
df_oversampled = pd.concat(
    [df_class_nonfraud, df_class_fraud_oversample], axis=0)
X = df_oversampled['tweets']
y = df_oversampled['Toxicity']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=None)

pipeline = Pipeline(steps=[('tfidf', TfidfVectorizer()),
                           ('model', SVC(C=10,
                                         gamma=0.1,
                                         kernel='sigmoid',
                                         random_state=42))])
pipeline.fit(X_train, y_train)

pickle.dump(pipeline, open('pipeline.pkl', 'wb'))
