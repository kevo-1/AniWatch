import requests
from Entities.Anime import Anime
from Entities.State import State
from Utilities.Logger import logger

url = "https://graphql.anilist.co"

def _getAnimeData(title, limit=20):
    query = """
    query ($search: String, $limit: Int) {
        Page(perPage: $limit) {
            media(search: $search, type: ANIME, isAdult: false){
                title {
                    romaji
                    english
                }
                episodes
                status
                format
                genres
                coverImage {
                    large
                }
            }
        }
    }
    """

    logger.info(f"Searching for anime: {title}")

    response = requests.post(url, json={"query": query, "variables": {"search": title, "limit": limit}})
    
    if response.status_code != 200:
        logger.error(f"API request failed with status {response.status_code}: {response.text}")
        return None

    AnimeList = []
    Results = response.json().get("data", {}).get("Page", {}).get("media", [])

    if not Results:
        logger.warning(f"No anime found for title: {title}")
        return None

    for media in Results:
        if "Ecchi" in media.get("genres", []):
            continue
        anime = Anime(
            title=media["title"].get("english") or media["title"].get("romaji"),
            numEp=media.get("episodes", 0),
            status=media.get("status", "Unknown"),
            genres=media.get("genres", []),
            cover=media["coverImage"].get("large", ""),
            current=State.Planned,
            anitype=media.get("format", "TV")
        )
        AnimeList.append(anime)

    return AnimeList

def searchAnime(title):
    return _getAnimeData(title)
