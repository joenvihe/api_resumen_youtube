from apiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import os
 
API_KEY = os.environ["API_KEY_YOUTUBE_DATA"]
# Set your API key and video ID
print(API_KEY)
VIDEO_ID = "5EfFqAAWvqw"
channel_id = 'Your Channel_id'  # replace it with your channel id
youtube = build('youtube', 'v3', developerKey=API_KEY)

try:
    responses = YouTubeTranscriptApi.get_transcript(VIDEO_ID, languages=['es'])
    print('\n'+"Video: "+"https://www.youtube.com/watch?v="+str(VIDEO_ID)+'\n'+'\n'+"Captions:")
    for response in responses:
        text = response['text']
        print(text)
except Exception as e:
    print(e)
