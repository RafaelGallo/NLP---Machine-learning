import json
import re
import tweepy
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from wordcloud import WordCloud
from textblob import TextBlob
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from datetime import datetime
from pylab import rcParams


api_key_twitter = '7afhFQjDvlhPYlRn93GnA8jeV'
api_secret_twitter = 'xgsaWTZ7Px7e32T0mnWFUaSUDQ8pjYTmG3Qab8GVU6Tro7f2MO'
api_access_token_twitter = '268456887-4kiBfTRLbLqWJSriyXAGAQeAf4QwDerjdtEYKfMb'
api_access_token_secret_twitter = 'D8z3zy6ZuW0DduOHcAPJiHcsFRWZqZCKdjniN5CDEodGE'

api = tweepy.OAuthHandler(api_key_twitter, api_secret_twitter)
api.set_access_token(api_access_token_twitter, api_access_token_secret_twitter)
api_twetter = tweepy.API(api, wait_on_rate_limit = True)


user_twitter = "pfizer"

tweets = tweepy.Cursor(api_twetter. user_timeline,
                        screen_name = user_twitter, 
                        count = None,
                        since_id = None,
                        max_id = None,
                        trim_user = True,
                        exclude_replies = True,
                        contributor_details = False,
                        include_entities = False
                        ).items(10000000000000000000000)

data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns = ["Tweet"])

# Limpeza de dados tweets
def clean_tweet(text):
    text = re.sub(r'@[A-Za-z0-9_]+', '', text)
    text = re.sub(r'#', '', text)
    text = re.sub(r'RT : ', '', text)
    text = re.sub(r'https?:\/\/[A-Za-z0-9\.\/]+', '', text)

    return text

data["Tweet"] = data["Tweet"].apply(clean_tweet)

def text_Subjectivity(txt):
    return TextBlob(txt).sentiment.subjectivity

def text_Polarity(txt):
    return TextBlob(txt).sentiment.polarity

data["Subjectivity"] = data["Tweet"].apply(text_Subjectivity)
data["Polarity"] = data["Tweet"].apply(text_Polarity)
data = data.drop(data[data['Tweet'] == ''].index)

def text_analysis(x):
    if x < 0:
        return "Negative"
    elif x == 0:
        return "Neutral"
    else:
        return "Positive"

data["Score"] = data["Polarity"].apply(text_analysis)

posi = data[data["Score"] == "Positive"]
obj = data[data["Subjectivity"] == 0]

label = data.groupby("Score").count().index.values
val = data.groupby("Score").size().values

# Salvando o dataset 
data.to_csv("pfizer.csv")
