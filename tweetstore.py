import couchdb
import couchdb.design

#Change this to point to location of couchdb server
DBURL = 'http://localhost:5984/'

class TweetStore(object):
    def __init__(self, dbname, url = DBURL):
        try:
            self.server = couchdb.Server(url=url)
            self.db = self.server.create(dbname)
        except couchdb.http.PreconditionFailed:
            self.db = self.server[dbname]
    
    def save_tweet(self, tw):
        tw['_id'] = tw['id_str']
        self.db.save(tw)