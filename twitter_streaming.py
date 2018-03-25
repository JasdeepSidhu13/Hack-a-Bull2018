
#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = "977617680818692101-kOKca0FlnSExUbaejyomKFiyE1cul20"
access_token_secret = "Pr0sMYYRIeys2bUUZS8xk5ac5UR3jUxeQaLrrNp5C9s1o"
consumer_key = "E6gxKXNfp5dHSw49RVGMboekr"
consumer_secret = "pmcT5qW04nutmTlasqICLMOrjFvLuvwWO5CTQHb5SpBgX5VZWq"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print (data)
        return True

    def on_error(self, status):
        print (status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['python', 'javascript', 'ruby'])
    