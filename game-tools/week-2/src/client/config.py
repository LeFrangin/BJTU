from enum import Enum

class Action( Enum ):
    START = 1
    RULE = 2
    SCORE = 3
    OBJECT = 4
    QUIT = 5

class State( Enum ):
    MENU = 1
    QUIT = 2