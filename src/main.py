from tweetFetcher import tweetFetcher
from confParser import confParser
import json, os

if __name__ == '__main__':
    # Get the current working directory
    cwd = os.getcwd()

    configParser = confParser()
    configResult = configParser.parseConfig()
    
    if configResult['ok'] != True:
        print(configResult['reason'])
    else:
        print("Config ok!")
        config = configResult['config']
        # Get the list of liked tweets
        fetcher = tweetFetcher(config['user_id'], config['bearer_token'])
        print("Getting list of liked tweets from Twitter...")
        tweets_json = fetcher.getLikedTweets()

        # For each liked tweet, get any media details
        print("Getting media details from liked tweets list...")
        tweet_media = fetcher.getTweetsMedia(tweets_json)
        tweet_urls = []
        print("Creating URL list for gallery-dl...")
        for tweet in tweet_media:
            # gallery-dl only needs the first photo/video url to 
            # download all of them in a tweet
            tweet_urls.append(tweet_media[tweet]['urls'][0])

        # Write the URLs to a file, for gallery-dl to use
        print("Writing URL list to file for gallery-dl...")
        with open('toDownload_temp.txt', 'w') as toDownload:
            for url in tweet_urls:
                toDownload.write(url + "\n")

        print("Attempting to download with gallery-dl...")
        # Download the URLs to the current working dir
        if 'gallery-dl_path' in config:
            os.system('cd %s && ./gallery-dl -d %s -i %s' % 
                (config['gallery-dl_path'], cwd, cwd + '/toDownload_temp.txt'))
        else:
            try:
                os.system('./gallery-dl -d %s -i %s' % (cwd, cwd + '/toDownload_temp.txt'))
            except:
                print('Couldn\'t find gallery-dl to download tweets!')
        
