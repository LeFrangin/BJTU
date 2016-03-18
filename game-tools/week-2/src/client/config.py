from enum import Enum

class Status( Enum ):
    RESULT = 1
    PLAYING = 2
    CHOOSING = 3
    WAITING = 4
    QUIT = 6
    MENU = 7
    RULE = 8
    SCORE = 9
    OBJECTS = 10
    CREDIT = 11

class Network( Enum ):
    ONLINE = 1
    OFFLINE = 2
    SEND = 3
    LISTEN = 4
    CONNECT = 5

class Result( Enum ):
    WIN = 1
    TIE = 0
    LOOSE = -1