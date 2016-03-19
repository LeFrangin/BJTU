from enum import Enum

class Status( Enum ):
    RESULT = 1
    PLAYING = 2
    CHOOSING = 3
    WAITING = 4
    UPDATE = 5
    QUIT = 6
    MENU = 7
    RULE = 8
    SCORE = 9
    OBJECTS = 10
    CREDIT = 11
    EDITOR = 12
    EDITORVIEW = 13

class Network( Enum ):
    ENTERROOM = 2
    LEAVEROOM = 1
    SELECTOBJECT = 3
    UPDATE = 5
    ADD = 6
    DELETE = 7
    ONLINE = 8
    OFFLINE = 9
    SEND = 10
    LISTEN = 11
    CONNECT = 12

class Result( Enum ):
    WIN = 1
    TIE = 0
    LOOSE = -1