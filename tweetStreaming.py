# -*- coding: utf-8 -*-
"""
Created on Sun May 22 14:58:48 2022

@author: ziongh
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 11:24:40 2019

@author: lealp
"""




import os
import pandas as pd
import tweepy
import json
def authenticate_tweetpy():
    with open("secrets.json", 'r') as f:
        secrets = json.load(f)

    return secrets


class TweetStreamer(tweepy.Stream):
    def __init__(self, file_name="tweets.txt", max_occurences=10, api=None):
        secrets = authenticate_tweetpy()
        super(TweetStreamer, self).__init__(secrets["consumer_key"],
                                            secrets["consumer_secret"],
                                            secrets["access_token"],
                                            secrets["access_token_secret"])
        self.num_tweets = 0
        self.file_name = file_name
        self.max_occurences = max_occurences

        if os.path.exists(self.file_name):
            pass
        else:
            self.file = open(self.file_name, "w")

    def on_status(self, status):
        tweet = status._json

        with open(self.file_name, 'a') as file:
            file.write(json.dumps(tweet) + '\n')
        self.num_tweets += 1
        if self.num_tweets < self.max_occurences:
            return True
        else:
            return False

    def on_error(self, status):
        print(status)


if "__main__" == __name__:
    # String of path to file: tweets_data_path
    tweets_data_path = os.path.join(os.getcwd(), 'Temp.csv')

    tStreamer = TweetStreamer(tweets_data_path)

    # Filter Twitter Streams to capture data by the keywords:
    tStreamer.filter(track=['Google Earth Engine'])

    # Initialize empty list to store tweets: tweets_data

    tweets_data = []
    # Open connection to file
    tweets_file = open(tweets_data_path, "r")

    # Read in tweets and store in list: tweets_data
    for line in tweets_file:
        tweet = json.loads(line)
        tweets_data.append(tweet)

    # create a df

    df = pd.DataFrame(tweets_data, columns=['text', 'lang'])
