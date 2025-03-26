from Entities.Anime import Anime
from Utilities.Logger import logger


class AniList:
    def __init__(self, loaded: list = []):
        self.WatchList: list[Anime] = [x for x in loaded]

    def AddAnime(self, anime: Anime):
        if anime not in self.WatchList:
            self.WatchList.append(anime)
            logger.info(f"Added Anime: {anime.Title}")
        else:
            logger.info(f"Anime Already Exists!")

    def RemoveAnime(self, anime: Anime):
        if anime in self.WatchList:
            self.WatchList.remove(anime)
            logger.info(f"Removed Anime: {anime.Title}")
        else:
            logger.info(f"Anime not Found in List")
            return
