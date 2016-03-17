import os, sys
import pygame
from pygame.locals import *
from config import Action

if not pygame.font: print( 'Warning, fonts disabled' )
if not pygame.mixer: print( 'Warning, sound disabled' )

class Client( object ):
	## The Client Class - This class handles the menu of the client.

	## variables
	__items = { "start": { "name":"Start a new game", "action": Action.START }, 
				"object": { "name":"Objects", "action": Action.OBJECT }, 
				"rule": { "name": "Rules", "action": Action.RULE }, 
				"score": { "name": "Scores", "action": Action.SCORE }, 
				"quit": { "name":"Quit", "action": Action.QUIT }  
			   }

	__colors = { "grey": ( 48, 56, 65 ), 
				 "grey1": (58, 71, 80), 
				 "hover": ( 3, 155, 229 ), 
				 "main": ( 246, 201, 14 ) 
				}

	__font = { "color": ( 255, 255, 255 ), "family": "ubuntumono", "size": 30, "bold": True }
	__action = None
	__screen = None
	
    
	def __init__( self, screen ):
		self.__screen = screen

	def reinit( self ):
		self.__action = None
		
	def display( self ):
		## reinit
		self.reinit()

		## Draw grid
		self.grid( "start", self.__screen.get_rect().width, 3, 1, 3, self.__colors[ "main" ] ) # Main block
		self.grid( "object", self.__screen.get_rect().width, self.__screen.get_rect().height, 2, 3, self.__colors[ "grey" ] ) # top left block
		self.grid( "score", 2, self.__screen.get_rect().height, 2, 3, self.__colors[ "grey1" ] ) # top right block
		self.grid( "rule", self.__screen.get_rect().width, 1.5, 2, 3, self.__colors[ "grey1" ] ) # bottom left block
		self.grid( "quit", 2, 1.5, 2, 3, self.__colors[ "grey" ] ) # bottom right block

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
			color = self.__colors[ "hover" ]
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