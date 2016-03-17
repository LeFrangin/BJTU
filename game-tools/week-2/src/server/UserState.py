from enum import Enum

class UserState(Enum):
    pending = 1
    playing = 2
    choosing = 3
    waiting = 4