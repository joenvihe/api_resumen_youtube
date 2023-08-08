import googleapiclient.discovery
import os

# Set your API key and video ID
API_KEY = os.environ["API_KEY_YOUTUBE_DATA"]
print(API_KEY)
VIDEO_ID = "5EfFqAAWvqw"

# Create a YouTube service object
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)
print(youtube)
# Call the captions.list method
captions_list_response = youtube.captions().list(
    part="snippet",
    videoId=VIDEO_ID,
).execute()

# Get the transcript for the first caption track
print(captions_list_response)
print("-----------------------------------------")
transcript = captions_list_response["items"][0]["snippet"]["text"]

# Print the transcript
print(transcript)