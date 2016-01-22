import urllib.request
import csv
import subprocess

def pullFeed():
    url = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.csv"
    return [line.decode('utf-8') for line in urllib.request.urlopen(url).readlines()]

def fetchNuclearRecords(contents):
    nuclearRecords = []
    for record in csv.reader(contents):
        for element in record:
            if "nuclear" in element:
                nuclearRecords.append(record)
    return nuclearRecords

def buildTweet(record):
    return "{0} magnitude nuclear explosion, {1}".format(record[4], record[13])

def compileTweets(nuclearRecords):
    tweets = []
    for record in nuclearRecords:
        tweets.append(buildTweet(record))
    return tweets

def getProcessOutput(myCommand):
    subprocess.call(myCommand)

def postTweet(tweet):
    tweet = tweet.replace("'", "\\'")
    getProcessOutput(["t", "update", tweet])

def updateTwitter():
    records = fetchNuclearRecords(pullFeed())
    tweets = compileTweets(records)
    for tweet in tweets:
        postTweet(tweet)

updateTwitter()
