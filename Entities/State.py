from enum import Enum

class State(Enum):
    Planned = 1
    Watching = 2
    Dropped = 3
    Completed = 4
    OnHold = 5