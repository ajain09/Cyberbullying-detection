import numpy as np
import pandas as pd
from flask import Flask
import pickle
import re
import sys


def process_tweet(tweet):
    return " ".join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])", " ", tweet.lower()).split())


app = Flask(__name__)
model = pickle.load(open('pipeline.pkl', 'rb'))

text = process_tweet(sys.argv[1])
text = pd.Series(text)
print(model.predict(text)[0])
sys.stdout.flush()

# if __name__ == "__main__":
#     app.run(port=5000, debug=True)
