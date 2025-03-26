from Entities.State import State

class Anime():
    def __init__(self, title: str, numEp: int, status: str, genres: dict, cover : str, current: State, anitype: str):
        self.Title = title
        self.NumberEp = numEp
        self.Status = status
        self.Genres = genres
        self.Cover = cover
        self.Current = current
        self.AniType = anitype

    def __eq__(self, anime: object) -> bool:
        if isinstance(anime, Anime):
            return self.Title == anime.Title
        return False

    def ChangeState(self, NewState: State):
        self.Current = NewState