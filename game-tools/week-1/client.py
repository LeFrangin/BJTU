import socket, select, string, sys, json, os, curses
from termcolor import colored
from enum import Enum

class Type( Enum ):
    MESSAGE = 1
    NAME = 2
    CHANNEL = 3

class Client( object ):

	## variables
	host = ""
	port = 0
	socket = None
	channel = ""
	name = ""
	color = ""
	stdscr = None

	## constructor
	def __init__( self ):
		pass

	## functions

	def init( self ):
		self.stdscr = curses.initscr()
		curses.nocbreak()
		stdscr.keypad( False )
		curses.echo()

	def displayMessage( self, message, name=None, color="white",clear=False ):
		if ( clear ):
			os.system( 'clear' )

		if ( name != None ):
			output = "<" + name + "> " + message + "\n"
		else:
			output = message + "\n"
		sys.stdout.write( colored( output, color ) );

	def prompt( self ):
		sys.stdout.write( "<" + self.name + "> " )

	def verifyArg( self ):
		if( len( sys.argv ) < 3 ):
			print( colored( 'Usage : python client.py hostname port', "red" ) );
			sys.exit()

	def changeYourUsername( self ):
		self.name = input( "Enter your little cute username : " )
		self.sendUsername( self.name )
		sys.stdout.write( colored( "\n*** your name has been changed to " + self.name + " ***\n\n", "cyan" ) );

	def changeYourChannel( self ):
		self.channel = input( "Enter the channel you want : " )
		self.sendChannel( self.channel )
		os.system( 'clear' )
		sys.stdout.write( colored( "*** your are into the channel " + self.channel + " ***\n\n", "cyan" ) );

	def serverConnection( self ):
		self.socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		self.socket.settimeout( 2 )
		try :
			self.socket.connect( ( self.host, self.port ) )
		except :
			print( 'Unable to connect' )
			sys.exit()

		# self.sendUsername( self.name )

		self.displayMessage( "*************************************************", clear=True )
		self.displayMessage( "                     Welcome                    " )
		self.displayMessage( "      Connected to remote host, let's chat      " )
		self.displayMessage( "    write *username* to change your username    " )
		self.displayMessage( "      write *channel* to change the channel     " )
		self.displayMessage( "      	write *exit* to quit the chat         " )
		self.displayMessage( "*************************************************\n" )

	def sendMessage( self, message ):
		self.socket.send( json.dumps( { 'type': 1, 'data': message } ).encode() )

	def sendUsername( self, message ):
		self.socket.send( json.dumps( { 'type': 2, 'data': message } ).encode() )

	def sendChannel( self, message ):
		self.socket.send( json.dumps( { 'type': 3, 'data': message } ).encode() )

	def letsChat( self ):
		while 1:
			socketList = [ sys.stdin, self.socket ]

			# Get the list sockets which are readable
			readSockets, writeSockets, errorSockets = select.select( socketList , [], [] )

			for sock in readSockets:
				#incoming message from remote server
				if sock == self.socket:
					buff = sock.recv( 4096 )
					if not buff :
						print( '\nDisconnected from chat server' )
						sys.exit()
					else :
						#print data from server
						data = json.loads( buff.decode() )

						if ( int( data[ "type" ] ) == 1 ):
							self.displayMessage( data[ "data" ], data[ "from" ] )
				#user entered a message
				else :
					message = sys.stdin.readline().replace( "\n", "" )
					if ( message == "*username*" ):
						self.changeYourUsername()
					elif ( message == "*channel*" ):
						self.changeYourChannel()
					elif ( message == "*exit*" ):
						self.displayMessage( "You have quit the chat, Bye bye", color="red" )
						sys.exit()
					elif ( len( message) > 0 ):
						self.sendMessage( message )
						# display my prompt
						# self.prompt()

	def run( self ):
		## verify arguments
		self.verifyArg();

		## init ncurse
		# self.init()

		## get parameters
		self.host = sys.argv[1]
		self.port = int( sys.argv[2] )

		## conenct to the server
		self.serverConnection()

		## change your name
		self.changeYourUsername()

		# json.loads('{"channel": "All", "type": 1, "data": "", "from": "anonymous"}')
		## begin the chat
		self.letsChat()



client = Client();
client.run();