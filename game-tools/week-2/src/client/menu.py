import os, sys
import pygame
from pygame.locals import *
from config import State
from helpers import Colors

if not pygame.font: print( 'Warning, fonts disabled' )
if not pygame.mixer: print( 'Warning, sound disabled' )

class Client( object ):
	## The Client Class - This class handles the menu of the client.

	## variables
	__items = { "start": { "name":"Start a new game", "action": State.PENDING }, 
				"object": { "name":"Objects", "action": State.OBJECTS }, 
				"credit": { "name":"Credit", "action": State.CREDIT }, 
				"rule": { "name": "Rules", "action": State.RULE }, 
				"score": { "name": "Scores", "action": State.SCORE }, 
				"quit": { "name":"Quit", "action": State.QUIT }  
			   }

	__colors = Colors()

	__font = { "color": ( 255, 255, 255 ), "family": "ubuntumono", "size": 30, "bold": True }
	__action = None
	__screen = None
	
    
	def __init__( self, screen ):
		self.__screen = screen

	def reinit( self ):
		self.__action = State.MENU
		
	def display( self ):
		## reinit
		self.reinit()

		## Draw grid
		self.grid( "start", self.__screen.get_rect().width, 3, 1.5, 3, self.__colors.get( "yellow" ) ) # Main block
		self.grid( "object", self.__screen.get_rect().width, self.__screen.get_rect().height, 2, 3, self.__colors.get( "grey" ) ) # top left block
		self.grid( "score", 2, self.__screen.get_rect().height, 2, 3, self.__colors.get( "grey1" ) ) # top right block
		self.grid( "credit", 1.5, 3, 3, 3, self.__colors.get( "grey" ) ) # Main block
		self.grid( "rule", self.__screen.get_rect().width, 1.5, 2, 3, self.__colors.get( "grey" ) ) # bottom left block
		self.grid( "quit", 2, 1.5, 2, 3, self.__colors.get( "grey1" ) ) # bottom right block

		return self.__action

	def grid( self, menu, xr, yr, widthR, heightR, color ):
		## Mouse position
		mouse = pygame.mouse.get_pos()

		## Set up variable according to the window size
		x = self.__screen.get_rect().width / xr
		y = self.__screen.get_rect().height / yr
		width = self.__screen.get_rect().width / widthR
		height = self.__screen.get_rect().height / heightR

		## Check if the mouse is hove the block
		if ( ( mouse[ 0 ] >= x and mouse[ 0 ] < ( x + width )  ) and ( mouse[ 1 ] >= y and mouse[ 1 ] < ( y + height )  ) ):
			color = self.__colors.get( "blue" )
			pygame.mouse.set_cursor( *pygame.cursors.tri_left )
			if ( pygame.mouse.get_pressed()[ 0 ] ):
				self.__action = self.__items[ menu ][ "action" ]

		## Draw rect and fill the background
		rect = pygame.draw.rect( self.__screen, color, ( x, y, width, height ), 2 )
		self.__screen.fill( color, rect )

		## Write menu text
		font = pygame.font.SysFont( self.__font[ "family" ], self.__font[ "size" ], self.__font[ "bold" ] )
		label = font.render( self.__items[ menu ][ "name" ], 1, self.__font[ "color" ] )
		x = x + ( width / 2 ) - ( label.get_rect().width / 2 )
		y = y + ( self.__screen.get_rect().height / 6 ) - ( label.get_rect().height / 2 )
		self.__screen.blit( label, ( x, y ) )