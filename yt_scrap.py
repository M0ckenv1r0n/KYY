import scrapetube
import tiktoken
from youtube_transcript_api import YouTubeTranscriptApi
import time


def get_transcript(username: str) -> tuple[str, int, int]:
    videos = list(scrapetube.get_channel(
        content_type='videos', channel_username=username)) #Creates a generator object of all videos' IDs, which is then converted to a list

    cum_video_count = len(videos)

    enc = tiktoken.get_encoding("cl100k_base")

    cum_tokens_amount = 0
    counter = 0
    transcripts = []

    for video_id in videos:
        try:
            subtitles_dict = YouTubeTranscriptApi.get_transcript(
                str(video_id['videoId']))
        except Exception as e:
            print(e) #change with logging
            continue

        subtitles_str = ' '.join(map(lambda x: x['text'], subtitles_dict))

        cum_tokens_amount += len(enc.encode(subtitles_str))

        if cum_tokens_amount > 100000:
            break

        title = video_id['title']['runs'][0]['text']

        transcripts.append(f"\'title: {title},'transcript': {subtitles_str}\'")

        if counter == 30:
            time.sleep(2)
        counter += 1
        time.sleep(2)

    transcripts = '\n\n'.join(transcripts)
    available_video = counter

    return (transcripts, available_video, cum_video_count)
