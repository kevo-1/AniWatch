import requests
import logging
from Entities.Anime import Anime
from Entities.State import State

# Configure logging
logging.basicConfig(
    filename="D:/Projects/AniWatch/animelogs.log",  
    level=logging.INFO,          
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def GetAnimeData(title):
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
    logging.info(f"Searching for anime: {title}")

    response = requests.post(url, json={"query": query, "variables": {"search": title}})
    
    if response.status_code != 200:
        logging.error(f"API request failed with status {response.status_code}: {response.text}")
        return None

    data = response.json().get("data", {}).get("Media")
    if not data:
        logging.warning(f"No anime found for title: {title}")
        return None

    anime = Anime(
        title=data["title"].get("english") or data["title"].get("romaji"),
        NumEp=data.get("episodes", 0),
        status=data.get("status", "Unknown"),
        genres=data.get("genres", []),
        cover=data["coverImage"].get("large", ""),
        current=State.Planned
    )

    logging.info(f"Anime found: {anime.Title}, Episodes: {anime.NumberEp}")
    return anime

def SearchAnime(title):
    return GetAnimeData(title)
