import socket, select, string, sys, json, os
from termcolor import colored

class Network( object ):
	## The network class - This class handles the network for the client/editor.

	## variables
	__host = "localhost"
	__port = 5000
	__socket = None
    
	def __init__( self ):
		pass

	def connect( self ):
		self.__socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		self.__socket.settimeout( 2 )
		try :
			self.__socket.connect( ( self.__host, self.__port ) )
		except :
			print( colored( 'Unable to connect to the remote server... try again :)', "red" ) )
			sys.exit()

	def sendMessage( self, message ):
		self.socket.send( json.dumps( { 'type': 1, 'data': message } ).encode() )
