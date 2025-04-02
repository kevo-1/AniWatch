import json

from Storage.AniList import AniList
from Entities.Anime import Anime
from Entities.State import State
from Utilities.Logger import logger

class StorageMan:
    def __init__(self):
        self.ListPath = "Storage/anilist.json"
    
    def LoadList(self, aniList: AniList):
        try:
            with open(self.ListPath, 'r') as file:
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
            aniList.AddAnime(anime = anime)

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

        with open(self.ListPath, 'w') as file:
            file.write(json.dumps(data, indent=4))
            logger.info("Saved List Successfully")
        file.close()
