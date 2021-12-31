import requests
import re

class tweetFetcher:
    def __init__(self, uId, bearerToken):
        self.uId = uId
        self.bearerToken = bearerToken
        self.headers = {'Authorization': 'Bearer ' + self.bearerToken,}
        
    def getLikedTweets(self):
        endpointUrl = 'https://api.twitter.com/2/users/' + self.uId + '/liked_tweets'
        response = requests.request("GET", endpointUrl, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error, got code: " + response.status_code)
    
    def getTweetsMedia(self, tweetIds):
        tweetMedia = {} # Hold tweet ID and media ID for that tweet
        endpointUrlStart = 'https://api.twitter.com/2/tweets?ids='
        endpointUrlEnd = '&tweet.fields=author_id,entities'
        
        # Will be a list of lists, for batches of IDs to process
        Ids = self.__createLists(tweetIds)
        for batch in Ids:
            response = requests.request("GET", endpointUrlStart + str(batch)[2:-2] + endpointUrlEnd, headers=self.headers)
            for tweet in response.json()['data']:
                if (('entities' in tweet) and ('urls' in tweet['entities'])):
                    relevantUrls = self.__extractUrls(tweet)
                    if(len(relevantUrls) > 0):
                        tweetMedia[tweet['id']] = {'author_id': tweet['author_id'], 'tweet_id': tweet['id'], 'urls': relevantUrls}
        return tweetMedia

    # Return a list of relevant URLs, which are URLs that contain
    # a link to a photo/video attached to the tweet
    def __extractUrls(self, tweet):
        mediaList = []
        
        for url in tweet['entities']['urls']:
            if ('expanded_url' in url) and (re.search('status\/\d+\/photo|video', url['expanded_url']) != None):
                mediaList.append(url['expanded_url'])
        return mediaList


    def __createLists(self, tweetIds):
        Ids = []
        toReturn = []
        chunksize = 100
        for tweet in tweetIds['data']:
            Ids.append(tweet['id'])

        # Twitter allows up to 100 IDs to be sent in 1 go. Will need to split
        # into batches of 100 if there's more than 100 IDs to be processed
        if len(Ids) < chunksize:
            toReturn.append([",".join(Ids)])
        else:
            for i in range(0, len(Ids), chunksize):
                toReturn.append([",".join(Ids[i:i+chunksize])])
        return toReturn

