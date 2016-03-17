import socket, select, string, sys, json, os
from termcolor import colored
from config import State, Result
from pygame.locals import *
import pygame

class Network( object ):
	## The network class - This class handles the network for the client/editor.

	## variables
	__host = "localhost"
	__port = 5000
	__socket = None
    
	def __init__( self ):
		pass

	## Connect to the server
	def connect( self ):
		self.__socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		self.__socket.settimeout( 2 )
		try :
			self.__socket.connect( ( self.__host, self.__port ) )
		except :
			print( colored( 'Unable to connect to the remote server... try again :)', "red" ) )
			sys.exit()

	## Send a message to the server
	def sendMessage( self, message ):
		self.socket.send( json.dumps( { 'type': 1, 'data': message } ).encode() )

class Colors( object ):
	## The color class - This class handles all colors value.

	## variables
	__colors = { 
		"grey": ( 48, 56, 65 ), 
		"grey1": (58, 71, 80), 
		"blue": ( 3, 155, 229 ), 
		"yellow": ( 246, 201, 14 ),
		"white": ( 255, 255, 255 ),
		"red": ( 211, 47 ,47 )
	}

	def __init__( self ):
		pass

	def get( self, name ):
		return self.__colors[ name ]

class Sounds( object ):
	## The sound class - This class handles all sounds in the game.

	## variables
	__urlToSound = os.path.dirname(__file__) + '/../../sounds/'
	__sounds = { 
		"looser" : { "isPlayed": False, "file": "looser.mp3" },
		"tie" : { "isPlayed": False, "file": "tie.mp3" },
		"win" : { "isPlayed": False, "file": "win.mp3" }
	}

	def __init__( self ):
		pass

	def play( self, sound ):
		if ( self.__sounds[ sound ][ "isPlayed" ] == False ):
			pygame.mixer.music.load( os.path.join( self.__urlToSound, self.__sounds[ sound ][ "file" ] ) )
			pygame.mixer.music.play()
			self.__sounds[ sound ][ "isPlayed" ] = True
			