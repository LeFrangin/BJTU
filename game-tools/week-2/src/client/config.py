from enum import Enum

class State( Enum ):
    PENDING = 1
    PLAYING = 2
    CHOOSING = 3
    WAITING = 4
    RESULT = 5
    QUIT = 6
    MENU = 7
    RULE = 8
    SCORE = 9
    OBJECTS = 10
    CREDIT = 11

class Result( Enum ):
    WIN = 1
    TIE = 2
    LOOSE = 3