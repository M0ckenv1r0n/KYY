import scrapetube
from youtube_transcript_api import YouTubeTranscriptApi 
import time
import tiktoken



# def username_type(username: str) -> str:
#                for param in ['channel_url', 'channel_username', 'channel_id']:
#                     try:
#                          videos = list(scrapetube.get_channel(
#                               content_type='videos', **{param: username}, limit=1))
#                          if videos:
#                               return param
#                     except Exception as e:
#                          logging.error(f"Error retrieving videos with {param}: {e}")
#                return False

import scrapetube
import tiktoken
from youtube_transcript_api import YouTubeTranscriptApi
import time

def get_transcript(username: str) -> tuple[str, int, int]:
    videos = list(scrapetube.get_channel(content_type='videos', channel_username = username))

    cum_video_count = len(videos)
    
    enc = tiktoken.get_encoding("cl100k_base")

    cum_tokens_amount = 0
    counter = 0
    transcripts = []

    for video_id in videos:
        if counter==1:
            break 
        subtitles_dict = YouTubeTranscriptApi.get_transcript(str(video_id['videoId']))

        subtitles_str = ' '.join(map(lambda x: x['text'], subtitles_dict))

        cum_tokens_amount += len(enc.encode(subtitles_str))


        if cum_tokens_amount > 100000:
            break

        title = video_id['title']['runs'][0]['text']

        transcripts.append (f"\'title: {title},'transcript': {subtitles_str}\'")

        if counter == 30:
            time.sleep(2)
        counter += 1
        time.sleep(2)
    
    
    transcripts = '\n\n'.join(transcripts)
    available_video = counter
    

    return (transcripts, available_video, cum_video_count)



          