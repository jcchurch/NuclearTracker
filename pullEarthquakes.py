import urllib.request
import csv
import subprocess

def pullFeed():
    """Pulls the 24 feed of all earthquakes"""
    url = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.csv"
    return [line.decode('utf-8') for line in urllib.request.urlopen(url).readlines()]

def fetchNuclearRecords(contents):
    """Filters out the feed contents to just records containing "nuclear"."""
    nuclearRecords = []
    for record in csv.reader(contents):
        for element in record:
            if "nuclear" in element:
                nuclearRecords.append(record)
    return nuclearRecords

def buildTweet(record):
    """Translates a record into a tweet."""
    return "{0} magnitude nuclear explosion, {1}".format(record[4], record[13])

def compileTweets(nuclearRecords):
    """Takes each nuclear tweet passes it over the buildTweet function."""
    return [buildTweet(record) for record in nuclearRecords]

def postTweet(tweet):
    """Posts the tweet with a call to 't'."""
    tweet = tweet.replace("'", "\\'")
    subprocess.call(["t", "update", tweet])

def updateTwitter():
    """Updates twitter with every instance of a nuclear explosion."""
    records = fetchNuclearRecords(pullFeed())
    tweets = compileTweets(records)
    for tweet in tweets:
        postTweet(tweet)

if __name__=='__main__':
    updateTwitter()
