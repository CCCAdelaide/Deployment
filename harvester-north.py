## Tweet harvester 1.0
## Daniel Teh
import tweepy, json
from tweetstore import TweetStore

storage = TweetStore('tweets_adelaide')

## OAuth Keys
# Application Key
consumer_key = "pSFHu1r2xAbqtbOsVvOU5vuFP"
consumer_key_secret = "hjMn6oCPCyBUanidBwAImXX051ILf1JVhrW4IO268qZS00IFvI"
# Daniel's personal twitter account key (DON'T GET ME BANNED PLEASE)
access_token = "19472785-vQJRKwqBNuOMs1s5AwTzv3wFWQlqtjeIflj5rNuyy"
access_token_secret = "R88rhzJBF3Rr85HDHn5kMKRkSmOEGKLJAO4mDrtK2ic7C"

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
        stream.filter(locations=[138.213501,-34.953493,139.070435,-34.492975])
    except Exception as e:
        print e
        start()
    
start()
 




