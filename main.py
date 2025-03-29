from DataFetch.ReteriveAni import searchAnime
from Storage.AniList import AniList
from Storage.StorageManager import StorageMan
from Entities.State import State
from DataFetch.ImageFetch import GetImage

man = StorageMan()
anilist = AniList()
man.LoadList(aniList=anilist)
ani = searchAnime('Code gease')
for anime in ani:
    print(anime.Title)
    GetImage(anime)
    anilist.AddAnime(anime=anime)
man.SaveList(aniList=anilist)