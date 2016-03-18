import socket, select, string, sys, json, os, time, fcntl
from termcolor import colored
from config import Status, Result, Network as net
from pygame.locals import *
import pygame
from threading import Thread

class Network( Thread ):
	## The network class - This class handles the network for the client/editor.

	## variables
	# __host = "localhost"
	__host = "192.168.1.102"
	__port = 5000
	__socket = None
	__bag = None
    
	def __init__( self, bag ):
		Thread.__init__( self )
		self.__functions = { net.CONNECT: self.connect, net.SEND: self.sendMessage, net.LISTEN: self.listen }
		self.__bag = bag

	## Connect to the server
	def run( self ):
		while self.__bag.status != Status.QUIT:
			if self.__bag.actionNetwork in self.__functions:
				self.__functions[ self.__bag.actionNetwork ]()

	## Connect to the server
	def connect( self ):
		self.__socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		self.__socket.settimeout( 0.5 )
		try :
			self.__socket.connect( ( self.__host, self.__port ) )
			self.__bag.statusNetwork = net.ONLINE
			self.__bag.actionNetwork = net.LISTEN
			fcntl.fcntl( self.__socket, fcntl.F_SETFL, os.O_NONBLOCK )
		except :
			print( colored( 'Unable to connect to the remote server... try again :)', "red" ) )
			self.__bag.statusNetwork = net.OFFLINE

	def listen( self ):
		socketList = [ self.__socket ]

		# Get the list sockets which are readable
		# readSockets, writeSockets, errorSockets = select.select( socketList , [], [] )

		try:
			msg = self.__socket.recv( 4096 )
		except:
			pass
			# print( "Nothing to do" )
		else:
			if not msg :
				print( '\nDisconnected from server' )
				self.__bag.statusNetwork = net.OFFLINE
				self.__bag.actionNetwork = net.CONNECT
				self.__status = Status.MENU
			else:
				data = json.loads( msg.decode() )
				if "result" in data:
					self.__bag.result = data[ "result" ]
				self.__bag.status = Status( data[ "state" ] )
				print( data )

	## Send a message to the server
	def sendMessage( self ):
		self.__socket.send( json.dumps( self.__bag.messageNetwork ).encode() )
		print("Hello j'envoie")
		self.__bag.actionNetwork = net.LISTEN
		self.__bag.messageNetwork = ""

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
			pygame.mixer.music.play( 1 )
			self.__sounds[ sound ][ "isPlayed" ] = True
			