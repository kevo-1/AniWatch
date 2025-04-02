import os
import requests
from Entities.Anime import Anime
from Utilities.Logger import logger

DefaultPath = r'Storage/AnimeCover/'

def sanitize_filename(name: str) -> str:
    return "".join(c if c.isalnum() or c in " _-" else "_" for c in name)

def GetImage(anime: Anime):
    SanitizedTitle = sanitize_filename(anime.Title)
    SaveAs = os.path.join(DefaultPath, f'{SanitizedTitle}.jpg')

    if CheckDownloads(anime.Title):
        logger.info("Cover Image already downloaded")
        return SaveAs
    else:
        try:
            with requests.get(anime.Cover, timeout=10) as response:
                response.raise_for_status()
                with open(SaveAs, 'wb') as image:
                    image.write(response.content)
                return SaveAs
        except requests.RequestException as e:
            logger.error(f"Error downloading {anime.Title}: {e}")
            return None

def CheckDownloads(title: str) -> bool:
    NewTitle = sanitize_filename(title)
    return os.path.exists(os.path.join(DefaultPath, f'{NewTitle}.jpg'))
