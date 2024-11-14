from openai import OpenAI
from config.logging_config import logger
import scrapetube


# Check if the provided username corresponds to a valid YouTube channel.
def valid_username(username: str) -> bool:
    try:
        videos = list(scrapetube.get_channel(
        content_type='videos', channel_username=username,limit=1))
        if videos:
            logger.info("YouTube credentials are valid!")
            return True
    except Exception as e:
        logger.error(f"Error retrieving videos: {e}")
        return False

    '''Solution that accepts also channel_url and channel_id, but ineffective coz username is used later'''
    # for param in ['channel_url', 'channel_username', 'channel_id']:
    #     try:
    #         videos = list(scrapetube.get_channel(
    #             content_type='videos', **{param: username}, limit=1))
    #         if videos:
    #             logger.info("YouYube credentials are valid!")
    #             return True
    #     except Exception as e:
    #         logger.error(f"Error retrieving videos with {param}: {e}")
    # return False


# Validate the OpenAI API key by checking the available models.
def check_api(openai_key: str) -> bool:
    try:
        client = OpenAI(api_key=openai_key)
        client.models.list()
        logger.info("API key is valid!")
        return True
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return False