import os
import sys
import time
import json
import requests
from requests_oauthlib import OAuth1

MEDIA_ENDPOINT_URL = 'https://upload.twitter.com/1.1/media/upload.json'
POST_TWEET_URL = 'https://api.twitter.com/1.1/statuses/update.json'

# 自分のAPI鍵
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

# アップロードする動画ファイルのパス
# VIDEO_FILENAME =  "/Users/shukubota/Desktop/media/short.mp4"
VIDEO_FILENAME = "/Users/shukubota/Desktop/media/598hmt-010_20220916T184301.mp4"

# API認証
oauth = OAuth1(os.environ['TWITTER_API_KEY'],
               client_secret=os.environ['TWITTER_API_SECRET'],
               resource_owner_key=os.environ['ACCESS_TOKEN'],
               resource_owner_secret=os.environ['ACCESS_TOKEN_SECRET'])

# twitter = OAuth1Session(os.environ['TWITTER_API_KEY'], os.environ['TWITTER_API_SECRET'], os.environ['ACCESS_TOKEN'], os.environ['ACCESS_TOKEN_SECRET'])
#

class VideoTweet(object):

    def __init__(self, file_name):
        '''
        Defines video tweet properties
        '''
        self.video_filename = file_name
        self.total_bytes = os.path.getsize(self.video_filename)
        self.media_id = None
        self.processing_info = None


    def upload_init(self):
        '''
        Initializes Upload
        '''
        print('INIT')

        request_data = {
            'command': 'INIT',
            'media_type': 'video/mp4',
            'total_bytes': self.total_bytes,
            'media_category': 'tweet_video'
        }

        req = requests.post(url=MEDIA_ENDPOINT_URL, data=request_data, auth=oauth)
        media_id = req.json()['media_id']

        self.media_id = media_id

        print('Media ID: %s' % str(media_id))


    def upload_append(self):
        '''
        Uploads media in chunks and appends to chunks uploaded
        '''
        segment_id = 0
        bytes_sent = 0
        file = open(self.video_filename, 'rb')

        while bytes_sent < self.total_bytes:
            chunk = file.read(4*1024*1024)

            print('APPEND')

            request_data = {
                'command': 'APPEND',
                'media_id': self.media_id,
                'segment_index': segment_id
            }

            files = {
                'media':chunk
            }

            req = requests.post(url=MEDIA_ENDPOINT_URL, data=request_data, files=files, auth=oauth)

            if req.status_code < 200 or req.status_code > 299:
                print(req.status_code)
                print(req.text)
                sys.exit(0)

            segment_id = segment_id + 1
            bytes_sent = file.tell()

            print('%s of %s bytes uploaded' % (str(bytes_sent), str(self.total_bytes)))

        print('Upload chunks complete.')


    def upload_finalize(self):
        '''
        Finalizes uploads and starts video processing
        '''
        print('FINALIZE')

        request_data = {
            'command': 'FINALIZE',
            'media_id': self.media_id
        }

        req = requests.post(url=MEDIA_ENDPOINT_URL, data=request_data, auth=oauth)
        print(req.json())

        self.processing_info = req.json().get('processing_info', None)
        self.check_status()


    def check_status(self):
        '''
        Checks video processing status
        '''
        if self.processing_info is None:
            return

        state = self.processing_info['state']

        print('Media processing status is %s ' % state)

        if state == u'succeeded':
            return

        if state == u'failed':
            sys.exit(0)

        check_after_secs = self.processing_info['check_after_secs']

        print('Checking after %s seconds' % str(check_after_secs))
        time.sleep(check_after_secs)

        print('STATUS')

        request_params = {
            'command': 'STATUS',
            'media_id': self.media_id
        }

        req = requests.get(url=MEDIA_ENDPOINT_URL, params=request_params, auth=oauth)

        self.processing_info = req.json().get('processing_info', None)
        self.check_status()


    def tweet(self):
        '''
        Publishes Tweet with attached video
        '''
        request_data = {
            'status': '良さげ',
            'media_ids': self.media_id
        }

        req = requests.post(url=POST_TWEET_URL, data=request_data, auth=oauth)
        print(req.json())
        print(req.json()['id'])

        reply_data = {
            'status': '作品はこちら！',
            'in_reply_to_status_id': req.json()['id']
        }
        requests.post(url=POST_TWEET_URL, data=reply_data, auth=oauth)

def tweet(event, context):
    print("=========tweet")
    print(event)
    print(context)
    # video_tweet = VideoTweet(VIDEO_FILENAME)
    # video_tweet.upload_init()
    # video_tweet.upload_append()
    # video_tweet.upload_finalize()
    # video_tweet.tweet()


# API経由で動画をアップロード
if __name__ == '__main__':
    videoTweet = VideoTweet(VIDEO_FILENAME)
    videoTweet.upload_init()
    videoTweet.upload_append()
    videoTweet.upload_finalize()
    videoTweet.tweet()

