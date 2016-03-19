import os, sys
import pygame
from pygame.locals import *
from config import Status, Network as net
from helpers import Colors
from threading import Thread

if not pygame.font: print( 'Warning, fonts disabled' )
if not pygame.mixer: print( 'Warning, sound disabled' )

class Client( object ):
	## The Client Class - This class handles the menu of the client.

	## variables
	__items = { "start": { "name":"Start a new game", "action": { "state": net.ENTERROOM.value }, "request": True }, 
				"offline": { "name":"Server offline :(", "action": Status.MENU, "request": False }, 
				"object": { "name":"Objects", "action": Status.OBJECTS, "request": False }, 
				"credit": { "name":"Credit", "action": Status.CREDIT, "request": False }, 
				"rule": { "name": "Rules", "action": Status.RULE, "request": False }, 
				# "score": { "name": "Score", "action": Status.SCORE, "request": False }, 
				"editor": { "name": "Editor", "action": Status.EDITOR, "request": False }, 
				"quit": { "name":"Quit", "action": Status.QUIT, "request": False }  
			   }
	__colors = Colors()
	__bag = None
	__font = { "color": ( 255, 255, 255 ), "family": "ubuntumono", "size": 30, "bold": True }
	__pressed = None
	
    
	def __init__( self, bag ):
		# Thread.__init__( self )
		self.__bag = bag

	def run( self ):
		while self.__bag.status != Status.QUIT:
			self.__bag.clock.tick( 60 )
			if ( self.__bag.status == Status.MENU ):
				self.display()

	def reinit( self ):
		self.__bag.status = Status.MENU
		self.__pressed = None
		
	def display( self ):
		## reinit
		self.reinit()

		## Draw grid
		if ( self.__bag.statusNetwork == net.ONLINE ):
			self.grid( "start", self.__bag.screen.get_rect().width, 3, 1.5, 3, self.__colors.get( "yellow" ) ) # Main block
		else:
			self.grid( "offline", self.__bag.screen.get_rect().width, 3, 1.5, 3, self.__colors.get( "red" ) ) # Main block
		self.grid( "object", self.__bag.screen.get_rect().width, self.__bag.screen.get_rect().height, 2, 3, self.__colors.get( "grey" ) ) # top left block
		if ( self.__bag.statusNetwork == net.ONLINE ):
			self.grid( "editor", 2, self.__bag.screen.get_rect().height, 2, 3, self.__colors.get( "grey1" ) ) # top right block
		else:
			self.grid( "offline", 2, self.__bag.screen.get_rect().height, 2, 3, self.__colors.get( "red" ) ) # top right block
		self.grid( "credit", 1.5, 3, 3, 3, self.__colors.get( "grey" ) ) # Main block
		self.grid( "rule", self.__bag.screen.get_rect().width, 1.5, 2, 3, self.__colors.get( "grey" ) ) # bottom left block
		self.grid( "quit", 2, 1.5, 2, 3, self.__colors.get( "grey1" ) ) # bottom right block

	def grid( self, menu, xr, yr, widthR, heightR, color ):
		## Mouse position
		mouse = pygame.mouse.get_pos()

		## Set up variable according to the window size
		x = self.__bag.screen.get_rect().width / xr
		y = self.__bag.screen.get_rect().height / yr
		width = self.__bag.screen.get_rect().width / widthR
		height = self.__bag.screen.get_rect().height / heightR

		## Check if the mouse is hove the block
		if ( ( mouse[ 0 ] >= x and mouse[ 0 ] < ( x + width )  ) and ( mouse[ 1 ] >= y and mouse[ 1 ] < ( y + height )  ) ):
			color = self.__colors.get( "blue" )
			pygame.mouse.set_cursor( *pygame.cursors.tri_left )
			if ( pygame.mouse.get_pressed()[ 0 ] and self.__pressed != menu ):
				if not self.__items[ menu ][ "request" ]:
					self.__bag.status = self.__items[ menu ][ "action" ]
				else:
					self.__bag.actionNetwork = net.SEND
					self.__bag.messageNetwork = self.__items[ menu ][ "action" ]
				self.__pressed = menu

		## Draw rect and fill the background
		rect = pygame.draw.rect( self.__bag.screen, color, ( x, y, width, height ), 2 )
		self.__bag.screen.fill( color, rect )

		## Write menu text
		font = pygame.font.SysFont( self.__font[ "family" ], self.__font[ "size" ], self.__font[ "bold" ] )
		label = font.render( self.__items[ menu ][ "name" ], 1, self.__font[ "color" ] )
		x = x + ( width / 2 ) - ( label.get_rect().width / 2 )
		y = y + ( self.__bag.screen.get_rect().height / 6 ) - ( label.get_rect().height / 2 )
		self.__bag.screen.blit( label, ( x, y ) )