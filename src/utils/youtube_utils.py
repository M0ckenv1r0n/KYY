import scrapetube
import tiktoken
from youtube_transcript_api import YouTubeTranscriptApi
import time
from config.logging_config import logger
from ..config.settings import LANGUAGES_LIST


'''
Retrieves the transcript for the latest posted video on a YouTube channel. Assumes the video's language 
matches the language of any other video on the same channel. Attempts to fetch the transcript in each 
language specified in 'LANGUAGES_LIST'. If a transcript is successfully retrieved, returns the language 
code. If no transcript is available in the specified languages, returns None.
'''


def get_subtitles_language(video_id: str) -> str:
    for lang in LANGUAGES_LIST:
        try:
            subtitles_dict = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
            logger.info(f"Language successfully determined: {lang}")
            return [lang]
        except Exception as e:
            continue

    logger.error(f"Language cannot be determined. The language is not in {LANGUAGES_LIST} | Error: {e}")
    return None


def get_transcript(username: str) -> tuple[str, int, int]:
    videos = list(scrapetube.get_channel(
        content_type='videos', channel_username=username)) #Creates a generator object of all videos

    cum_video_count = len(videos)

    lang = get_subtitles_language(str(videos[0]['videoId']))

    enc = tiktoken.get_encoding("cl100k_base")

    counter = 0
    cum_tokens_amount = 0

    transcripts = []

    for video_id in videos:
        try:
            subtitles_dict = YouTubeTranscriptApi.get_transcript(str(video_id['videoId']), languages = lang)
        except Exception as e:
            logger.error(e)
            continue

        subtitles_str = ' '.join(map(lambda x: x['text'], subtitles_dict))

        cum_tokens_amount += len(enc.encode(subtitles_str))

        if cum_tokens_amount > 100000:
            break

        title = video_id['title']['runs'][0]['text']

        transcripts.append(f"\'title: {title},'transcript': {subtitles_str}\'")

        counter += 1
        time.sleep(2)

    transcripts = '\n\n'.join(transcripts)
    available_video = counter

    return (transcripts, available_video, cum_video_count)
