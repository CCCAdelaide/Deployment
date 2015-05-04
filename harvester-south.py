## Tweet harvester 1.0
## Daniel Teh
import tweepy, json
from tweetstore import TweetStore

storage = TweetStore('tweets_adelaide')

## OAuth Keys
# Application Key
consumer_key = "Jgu6HGiLr8lZCvRLeCxuRNphO"
consumer_key_secret = "TRpm5QNjMeTIemwO2S8QrTT3vv5DHjvNnUseShm7Oniey8w9xm"
# David's personal twitter account key (DON'T GET ME BANNED PLEASE)
access_token = "3184873568-KAaeFPKVhXEVorENkK59mZBsmZVZfROCbppJzPt"
access_token_secret = "VV2slmCU1a0Ne3BDlkSv6MxU9cWb5OPYp5V5KAihTDJVS"

## Init OAuth
auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)

## Main
api = tweepy.API(auth)
print "Interface set up.."
            
class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        decoded = json.loads(data)
        storage.save_tweet(decoded)
        print '@%s: %s' %(decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
        print ""
        return True
    def on_error(self,status):
        print status

l = StdOutListener()
stream = tweepy.Stream(auth,l)

def start():
    print "*"*78
    print "Getting tweets from Adelaide"
    print "*"*78
    # use bboxfinder.com to figure out bounding boxes lat/long coordinates
    # DO NOT USE GOOGLE MAPS! (coordinates are flipped)
    try:
        stream.filter(locations=[138.213501,-35.395767,139.070435,-34.953493])
    except Exception as e:
        print e
        start()
    
start()
 




