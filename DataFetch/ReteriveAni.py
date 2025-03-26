import requests
from Entities.Anime import Anime
from Entities.State import State
from Utilities.Logger import logger

def _getAnimeData(title):
    url = "https://graphql.anilist.co"
    query = """
    query ($search: String) {
        Media(search: $search, type: ANIME) {
            title {
                romaji
                english
            }
            episodes
            status
            genres
            coverImage {
                large
            }
        }
    }
    """
    logger.info(f"Searching for anime: {title}")

    response = requests.post(url, json={"query": query, "variables": {"search": title}})
    
    if response.status_code != 200:
        logger.error(f"API request failed with status {response.status_code}: {response.text}")
        return None

    data = response.json().get("data", {}).get("Media")
    if not data:
        logger.warning(f"No anime found for title: {title}")
        return None

    anime = Anime(
        title=data["title"].get("english") or data["title"].get("romaji"),
        numEp=data.get("episodes", 0),
        status=data.get("status", "Unknown"),
        genres=data.get("genres", []),
        cover=data["coverImage"].get("large", ""),
        current=State.Planned
    )

    logger.info(f"Anime found: {anime.Title}, Episodes: {anime.NumberEp}")
    return anime

def searchAnime(title):
    return _getAnimeData(title)
