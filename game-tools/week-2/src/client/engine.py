import helpers
import sys, os, time
from pygame.locals import *
import pygame
from config import State, Result

class Game( object ):
	## The game class - This class handles game engine.

	## variables
	__screen = None
	__colors = helpers.Colors()
	__sounds = helpers.Sounds()
	__font = { "color": ( 255, 255, 255 ), "family": "ubuntumono", "size": 30, "bold": True }
	__waitBar = { "x": 0, "ratioX": 5, "width": 0, "ratioW": 10 }
	__objects = [ 
		{ "name":"Rock", "icon": "rock.png", "id": 1, "strengh": 10, "defense": 4, "realiability": 7 }, 
		{ "name":"Paper", "icon": "paper.png", "id": 2, "strengh": 3, "defense": 2, "realiability": 2 }, 
		{ "name": "Scissors", "icon": "scissors.png", "id": 3, "strengh": 6, "defense": 10, "realiability": 1 } 
	]
	__urlToIcons = os.path.dirname(__file__) + '/../../images/'
	__selectedObject = 0
	__informationObject = None

	def __init__( self, screen ):
		self.__screen = screen
		self.__waitBar[ "width" ] = self.__screen.get_rect().width / 2
		pygame.mouse.set_cursor( *pygame.cursors.tri_left )

	def drawMessage( self, message, x, y, center, size, color ):
		## Write a message
		font = pygame.font.SysFont( self.__font[ "family" ], size, self.__font[ "bold" ] )
		label = font.render( message, 1, self.__colors.get( color ) )
		if ( center ):
			x -= ( label.get_rect().width / 2 )
			y -= ( label.get_rect().height / 2 )
		self.__screen.blit( label, ( x, y ) )

	def drawRect( self, x, y, width, height, color ):
		## Draw rect and fill the background
		rect = pygame.draw.rect( self.__screen, self.__colors.get( color ), ( x, y, width, height ), 2 )
		self.__screen.fill( self.__colors.get( color ), rect )
		return rect

	def result( self, result ):

		# Write a message
		x = self.__screen.get_rect().width / 2
		y = ( self.__screen.get_rect().height / 2 )
		escape = "Press escape to continue"

		if ( result == Result.WIN ):
			self.drawRect( 0, 0, self.__screen.get_rect().width, self.__screen.get_rect().height, "blue" )
			self.drawMessage( "You win :)", x, y - ( self.__screen.get_rect().height / 9 ) , True, 50, "white" )
			self.drawMessage( escape, x, y + ( self.__screen.get_rect().height / 9 ) , True, 20, "white" )
			self.__sounds.play( "win" )
		elif ( result == Result.TIE ):
			self.drawRect( 0, 0, self.__screen.get_rect().width, self.__screen.get_rect().height, "grey" )
			self.drawMessage( "It's a tie !", x, y - ( self.__screen.get_rect().height / 9 ) , True, 50, "white" )
			self.drawMessage( escape, x, y + ( self.__screen.get_rect().height / 9 ) , True, 20, "white" )
			self.__sounds.play( "tie" )
		else:
			self.drawRect( 0, 0, self.__screen.get_rect().width, self.__screen.get_rect().height, "red" )
			self.drawMessage( "You loose :(", x, y - ( self.__screen.get_rect().height / 9 ) , True, 50, "white" )
			self.drawMessage( escape, x, y + ( self.__screen.get_rect().height / 9 ) , True, 20, "white" )
			self.__sounds.play( "looser" )

	def wait( self ):
		## Draw rect and fill the background
		self.drawRect( 0, 0, self.__screen.get_rect().width, self.__screen.get_rect().height, "grey" )

		# Write a message
		self.drawMessage( "Please wait for other players...", ( self.__screen.get_rect().width / 2 ), ( self.__screen.get_rect().height / 2 ) - ( self.__screen.get_rect().height / 9 ), True, self.__font[ "size" ], "white" )

		## Progression bar
		height = 20
		y = self.__screen.get_rect().height / 1.5
		self.drawRect( self.__waitBar[ "x" ], y, self.__waitBar[ "width" ], height, "yellow" )

		## Animation
		self.__waitBar[ "x" ] += self.__waitBar[ "ratioX" ]
		if ( self.__waitBar[ "x" ] > ( self.__screen.get_rect().width - self.__waitBar[ "width" ] ) ):
			self.__waitBar[ "ratioX" ] *= -1
		elif ( self.__waitBar[ "x" ] <= 0 ):
			self.__waitBar[ "ratioX" ] *= -1

	def objectInformations( self, object ):
		## Mouse position
		mouse = pygame.mouse.get_pos()

		width = self.__screen.get_rect().width / 6
		height = self.__screen.get_rect().height / 6

		for key, object in enumerate( self.__objects ):
			if ( ( mouse[ 0 ] >= object[ "x" ] and mouse[ 0 ] < ( object[ "x" ] + object[ "width" ] )  ) and ( mouse[ 1 ] >= object[ "y" ] and mouse[ 1 ] < ( object[ "y" ] + object[ "height" ] )  ) ):
				## Draw rect
				x = mouse[ 0 ]
				y = mouse[ 1 ]
				if ( x + width > self.__screen.get_rect().width ):
					x = mouse[ 0 ] - width

				## Draw rect
				rect = self.drawRect( x, y, width, height, "white" )

				## Draw message
				self.drawMessage( "Strengh : " + str( object[ "strengh" ] ), x + ( width / 2 ), y + 20, True, 20, "grey" )
				self.drawMessage( "Defense : " + str( object[ "defense" ] ), x + ( width / 2 ), y + ( height / 2 ), True, 20, "grey" )
				self.drawMessage( "Realiability : " + str( object[ "realiability" ] ), x + ( width / 2 ), y + height - 20, True, 20, "grey" )


	def objects( self, choosing ):
		## Mouse position
		mouse = pygame.mouse.get_pos()

		self.drawRect( 0, 0, self.__screen.get_rect().width, self.__screen.get_rect().height, "grey" )
		width = self.__screen.get_rect().width / 3
		height = self.__screen.get_rect().height / 3
		x = 0
		y = 0
		if ( choosing ):
			y = self.__screen.get_rect().height / 7
		count = 0
		imageSize = ( self.__screen.get_rect().width / 9 )

		## Draw title
		if ( choosing ):
			self.drawMessage( "Choose your weapon", self.__screen.get_rect().width / 2, self.__screen.get_rect().height / 15, True, 40, "white" )

		for key, object in enumerate( self.__objects ):
			try :
				## Load image
				image = pygame.image.load( os.path.join( self.__urlToIcons, object[ "icon" ] ) )
				image = pygame.transform.smoothscale( image, ( int( imageSize ), int( imageSize ) ) )

				## Create the rect
				if ( count % 2 == 0 ):
					color = "grey"
				else: 
					color = "grey1"

				## Check if the mouse is hove the block
				if ( ( mouse[ 0 ] >= x and mouse[ 0 ] < ( x + width )  ) and ( mouse[ 1 ] >= y and mouse[ 1 ] < ( y + height )  ) ):
					color = "blue"
					if ( choosing and pygame.mouse.get_pressed()[ 0 ] ):
						self.__selectedObject = object[ "id" ]

				if ( choosing and self.__selectedObject == object[ "id" ] ):
					color = "yellow"

				## Update Object position
				self.__objects[ key ][ "x" ] = x
				self.__objects[ key ][ "y" ] = y
				self.__objects[ key ][ "width" ] = width
				self.__objects[ key ][ "height" ] = height

				## Draw rect
				rect = self.drawRect( x, y, width, height, color )

				## Attach image to the rect
				self.__screen.blit( image, ( x + ( width / 2 ) - ( imageSize / 2 ), y + ( height / 2 ) - ( imageSize / 2 ) - 50 ) )

				## Draw message
				self.drawMessage( object[ "name" ], x + ( width / 2 ), y + ( height / 2 ) + ( imageSize / 2 ), True, self.__font[ "size" ], "white" )

				x += width
				if ( x > self.__screen.get_rect().width ):
					x = 0
					y += height
				## counter for the color	
				count += 1
			except :
				print( colored( 'Unable to connect to load the icon ' + self.__urlToIcons + object[ "icon" ], "red" ) )

		## Show informations about object
		self.objectInformations( object )