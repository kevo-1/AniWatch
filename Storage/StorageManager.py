import json
import os
from pathlib import Path 

from Storage.AniList import AniList
from Entities.Anime import Anime
from Entities.State import State
from Utilities.Logger import logger
from DataFetch.ImageFetch import sanitize_filename

class StorageMan:
    def __init__(self):
        self.ListPath = "Storage/anilist.json"
        Path("Storage").mkdir(parents=True, exist_ok=True)
        Path("AnimeCover").mkdir(parents=True, exist_ok=True)
    
    def LoadList(self, aniList: AniList):
        try:
            with open(self.ListPath, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        
        for iter in data:
            anime = Anime(
                title=iter["Title"],
                numEp=iter["NumberEp"],
                status=iter["Status"],
                genres=iter["Genres"],
                cover=iter["Cover"],
                current=State[iter["Current"]],
                anitype=iter["AniType"]
            )
            aniList.AddAnime(anime=anime)

    def SaveList(self, aniList: AniList):
        data = [
            {
                "Title": anime.Title,
                "NumberEp": anime.NumberEp,
                "Status": anime.Status,
                "Genres": anime.Genres,
                "Cover": anime.Cover,
                "Current": anime.Current.name,
                "AniType": anime.AniType
            }
            for anime in aniList.WatchList
        ]

        with open(self.ListPath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
            logger.info("Saved List Successfully")

    def CleanCovers(self, anilist: AniList) -> None:
        try:
            covers_dir = os.path.abspath("Storage/AnimeCover")
            
            used_covers = {
                os.path.join(covers_dir, f"{sanitize_filename(anime.Title)}.jpg")
                for anime in anilist.WatchList
                if anime.Cover
            }
            
            os.makedirs(covers_dir, exist_ok=True)
            
            for filename in os.listdir(covers_dir):
                if filename.lower().endswith(".jpg"):
                    full_path = os.path.join(covers_dir, filename)
                    try:
                        if full_path not in used_covers:
                            os.remove(full_path)
                            logger.info(f"Removed unused cover: {filename}")
                    except FileNotFoundError:
                        logger.debug(f"Cover already removed: {filename}")
                    except PermissionError:
                        logger.warning(f"Permission denied removing {filename}")
                    except Exception as e:
                        logger.error(f"Error removing {filename}: {str(e)}")
                        
        except Exception as e:
            logger.error(f"Error during cover cleanup: {str(e)}")