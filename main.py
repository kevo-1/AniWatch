from DataFetch.ReteriveAni import searchAnime
from Storage.AniList import AniList
from Storage.StorageManager import StorageMan
from Entities.State import State

man = StorageMan()
anilist = AniList()
man.LoadList(aniList=anilist)
for anime in anilist.WatchList:
    anime.ChangeState(State.Completed)
man.SaveList(aniList=anilist)