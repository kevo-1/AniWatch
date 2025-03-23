from Entities.State import State

class Anime():
    def __init__(self, title: str, NumEp: int, status: str, genres: dict, cover : str, current: State):
        self.Title = title
        self.NumberEp = NumEp
        self.Status = status
        self.Genres = genres
        self.Cover = cover
        self.Current = current

    def ChangeState(self, NewState: State):
        self.Current = NewState