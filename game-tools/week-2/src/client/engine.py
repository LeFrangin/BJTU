import helpers
import sys, os, time
from pygame.locals import *
import pygame
from config import Status, Result, Network as net
import xml.etree.cElementTree as ET
from termcolor import colored

class Game( object ):
	## The game class - This class handles game engine.

	## variables
	__bag = None
	__colors = helpers.Colors()
	__sounds = helpers.Sounds()
	__font = { "color": ( 255, 255, 255 ), "family": "ubuntumono", "size": 40, "bold": True }
	__waitBar = { "x": 0, "ratioX": 5, "width": 0, "ratioW": 10 }
	# __objects = [ 
	# 	{ "name":"Rock", "icon": "rock.png", "id": 1, "strengh": 10, "defense": 4, "realiability": 7 }, 
	# 	{ "name":"Paper", "icon": "paper.png", "id": 2, "strengh": 3, "defense": 2, "realiability": 2 }, 
	# 	{ "name": "Scissors", "icon": "scissors.png", "id": 3, "strengh": 6, "defense": 10, "realiability": 1 } 
	# ]
	__urlToIcons = os.path.dirname(__file__) + '/../../images/'
	__selectedObject = None
	__user = ET.ElementTree( file = os.path.dirname(__file__) + "/user.xml" ).getroot()
	__rules = ET.ElementTree( file = os.path.dirname(__file__) + "/rules.xml" ).getroot()
	__editor = { "new":  True }

	def __init__( self, bag ):
		self.__bag = bag
		self.__waitBar[ "width" ] = self.__bag.screen.get_rect().width / 2

	def reinit( self ):
		self.__selectedObject = None
		self.__bag.cursorPosition = 0
		self.__bag.attribute = None
		self.__bag.object = None

	def drawMessage( self, message, x, y, center, size, color, bold=True ):
		## Write a message
		font = pygame.font.SysFont( self.__font[ "family" ], size, bold )
		label = font.render( message, 1, self.__colors.get( color ) )
		if ( center ):
			x -= ( label.get_rect().width / 2 )
			y -= ( label.get_rect().height / 2 )
		self.__bag.screen.blit( label, ( x, y ) )

		return label

	def drawRect( self, x, y, width, height, color ):
		## Draw rect and fill the background
		rect = pygame.draw.rect( self.__bag.screen, self.__colors.get( color ), ( x, y, width, height ), 2 )
		self.__bag.screen.fill( self.__colors.get( color ), rect )
		return rect

	def drawObjects( self, title, selected ):
		## Mouse position
		mouse = pygame.mouse.get_pos()

		self.drawRect( 0, 0, self.__bag.screen.get_rect().width, self.__bag.screen.get_rect().height, "grey" )
		width = self.__bag.screen.get_rect().width / 3
		height = self.__bag.screen.get_rect().height / 3
		x = 0
		y = self.__bag.screen.get_rect().height / 7
		count = 0
		imageSize = ( self.__bag.screen.get_rect().width / 9 )

		## Draw title
		self.drawMessage( title, self.__bag.screen.get_rect().width / 2, self.__bag.screen.get_rect().height / 15, True, 40, "white" )

		for key, object in enumerate( self.__bag.objects ):
			try :
				## Load image
				image = pygame.image.load( os.path.join( self.__urlToIcons, object[ "image" ] ) )
				image = pygame.transform.smoothscale( image, ( int( imageSize ), int( imageSize ) ) )

				## Create the rect
				if ( count % 2 == 0 ):
					color = "grey"
				else: 
					color = "grey1"

				## Check if the mouse is hove the block
				if ( ( mouse[ 0 ] >= x and mouse[ 0 ] < ( x + width )  ) and ( mouse[ 1 ] >= y and mouse[ 1 ] < ( y + height )  ) ):
					color = "blue"
					if ( pygame.mouse.get_pressed()[ 0 ] ):
						self.__selectedObject = object[ "id" ]

				if ( selected and self.__selectedObject == object[ "id" ] ):
					color = "yellow"

				## Update Object position
				self.__bag.objects[ key ][ "x" ] = x
				self.__bag.objects[ key ][ "y" ] = y
				self.__bag.objects[ key ][ "width" ] = width
				self.__bag.objects[ key ][ "height" ] = height

				## Draw rect
				rect = self.drawRect( x, y, width, height, color )

				## Attach image to the rect
				self.__bag.screen.blit( image, ( x + ( width / 2 ) - ( imageSize / 2 ), y + ( height / 2 ) - ( imageSize / 2 ) - 50 ) )

				## Draw message
				self.drawMessage( object[ "name" ], x + ( width / 2 ), y + ( height / 2 ) + ( imageSize / 2 ), True, self.__font[ "size" ], "white" )

				x += width
				if ( ( x + width ) > self.__bag.screen.get_rect().width ):
					x = 0
					y += height
				## counter for the color	
				count += 1
			except :
				print( colored( 'Unable to connect to load the image ' + self.__urlToIcons + object[ "image" ], "red" ) )

	## All view from the game are implement here
	def result( self ):

		result = Result( self.__bag.result )
		# Write a message
		x = self.__bag.screen.get_rect().width / 2
		y = ( self.__bag.screen.get_rect().height / 2 )
		escape = "Press escape to continue"

		if ( result == Result.WIN ):
			self.drawRect( 0, 0, self.__bag.screen.get_rect().width, self.__bag.screen.get_rect().height, "blue" )
			self.drawMessage( "You win :)", x, y - ( self.__bag.screen.get_rect().height / 9 ) , True, 50, "white" )
			self.drawMessage( escape, x, y + ( self.__bag.screen.get_rect().height / 9 ) , True, 20, "white" )
			self.__sounds.play( "win" )
		elif ( result == Result.TIE ):
			self.drawRect( 0, 0, self.__bag.screen.get_rect().width, self.__bag.screen.get_rect().height, "grey" )
			self.drawMessage( "It's a tie !", x, y - ( self.__bag.screen.get_rect().height / 9 ) , True, 50, "white" )
			self.drawMessage( escape, x, y + ( self.__bag.screen.get_rect().height / 9 ) , True, 20, "white" )
			self.__sounds.play( "tie" )
		else:
			self.drawRect( 0, 0, self.__bag.screen.get_rect().width, self.__bag.screen.get_rect().height, "red" )
			self.drawMessage( "You loose :(", x, y - ( self.__bag.screen.get_rect().height / 9 ) , True, 50, "white" )
			self.drawMessage( escape, x, y + ( self.__bag.screen.get_rect().height / 9 ) , True, 20, "white" )
			self.__sounds.play( "looser" )

	def rule( self ):
		width = self.__bag.screen.get_rect().width
		height = self.__bag.screen.get_rect().height

		## Draw rect and fill the background
		self.drawRect( 0, 0, width, height, "grey" )

		## Write the title
		self.drawMessage( "Rules are very simple :)", ( width / 2 ), ( height / 9 ), True, self.__font[ "size" ], "white" )

		## Write rules
		count = 0
		for child in self.__rules:
			text = child.attrib[ "id" ] + ". " + child.text
			self.drawMessage( text, 50, ( height / 3 ) + count, False, 20, "white", False )
			count += 35

	def editor( self ):
		width = self.__bag.screen.get_rect().width
		height = self.__bag.screen.get_rect().height
		goToView = False

		if ( self.__bag.key == K_n ):
			self.__bag.object = { "name": "New Object", "strength": 0, "defense": 0, "reliability": 0, "image": "defaut.png" }
			self.__editor[ "new" ] = True
			goToView = True

		if self.__selectedObject != None:
			self.__editor[ "new" ] = False
			goToView = True
			for key, object in enumerate( self.__bag.objects ):
				if ( object[ "id" ] == self.__selectedObject ):
					self.__bag.object = object.copy()
					del self.__bag.object[ "x" ]
					del self.__bag.object[ "y" ]
					del self.__bag.object[ "width" ]
					del self.__bag.object[ "height" ]

		if goToView:
			self.__bag.status = Status.EDITORVIEW
			self.__bag.attribute = "strength"
			self.__bag.cursorLimit = 2

		## Draw objects
		self.drawObjects( "Manage all objects from here", True )

		## Show informations about object
		self.objectInformations()

	def editorView( self ):
		width = self.__bag.screen.get_rect().width
		height = self.__bag.screen.get_rect().height
		imageSize = ( height / 6 )

		if ( self.__bag.cursorPosition > self.__bag.cursorLimit ):
			self.__bag.cursorPosition = 0
		elif ( self.__bag.cursorPosition < 0 ):
			self.__bag.cursorPosition = self.__bag.cursorLimit

		if self.__bag.object == None:
			self.__bag.status = Status.EDITOR
		else:

			## Update Values
			if ( self.__bag.key == K_UP ):
				self.__bag.cursorPosition -= 1
			elif ( self.__bag.key == K_DOWN ):
				self.__bag.cursorPosition += 1
			elif ( self.__bag.key == K_LEFT ):
				self.__bag.object[ self.__bag.attribute ] -= 1
			elif ( self.__bag.key == K_RIGHT ):
				self.__bag.object[ self.__bag.attribute ] += 1
			elif ( self.__bag.key == K_RETURN ):
				self.__bag.actionNetwork = net.SEND
				if self.__editor[ "new" ]:
					self.__bag.messageNetwork = { "state": net.ADD.value, "object": self.__bag.object }
				else:
					self.__bag.messageNetwork = { "state": net.UPDATE.value, "object": self.__bag.object }
				self.reinit()
				self.__bag.key = None
				return
			elif ( self.__bag.key == K_DELETE ):
				self.__bag.actionNetwork = net.SEND
				self.__bag.messageNetwork = { "state": net.DELETE.value, "id": self.__bag.object[ "id" ] }
				self.reinit()
				self.__bag.key = None
				return
			elif self.__bag.key != None and self.__bag.key >= K_a and self.__bag.key <= K_z:
				self.__bag.object[ "name" ] += chr( self.__bag.key )
			elif self.__bag.key == K_BACKSPACE:
				self.__bag.object[ "name" ] = self.__bag.object[ "name" ][ :-1 ]

			## Adjust the cursor
			if ( self.__bag.cursorPosition == 0 ):
				self.__bag.attribute = "strength"
			elif ( self.__bag.cursorPosition == 1 ):
				self.__bag.attribute = "defense"
			elif ( self.__bag.cursorPosition == 2 ):
				self.__bag.attribute = "reliability"
			self.__bag.key = None

			## Draw rect and fill the background
			self.drawRect( 0, 0, width, height, "grey" )

			# Write the title
			self.drawMessage( self.__bag.object[ "name" ], ( width / 2 ), ( height / 9 ), True, self.__font[ "size" ], "white" )

			## Load image
			image = pygame.image.load( os.path.join( self.__urlToIcons, self.__bag.object[ "image" ] ) )
			image = pygame.transform.smoothscale( image, ( int( imageSize ), int( imageSize ) ) )

			## Draw image
			label = self.drawMessage( "Icon : ", 50, ( height / 4 ), False, 25, "white" )
			self.__bag.screen.blit( image, ( label.get_rect().width + 100, ( height / 4 ) - ( imageSize / 2 ) ) )

			## Draw attributes
			if self.__bag.cursorPosition == 0:
				label = self.drawMessage( "Strength : " + str( self.__bag.object[ "strength" ] ), 50, ( height / 4 ) + 100, False, 25, "blue" )
			else:
				label = self.drawMessage( "Strength : " + str( self.__bag.object[ "strength" ] ), 50, ( height / 4 ) + 100, False, 25, "white" )

			if self.__bag.cursorPosition == 1:
				label = self.drawMessage( "Defense : " +  str( self.__bag.object[ "defense" ]), 50, ( height / 4 ) + 200, False, 25, "blue" )
			else:
				label = self.drawMessage( "Defense : " + str( self.__bag.object[ "defense" ] ), 50, ( height / 4 ) + 200, False, 25, "white" )

			if self.__bag.cursorPosition == 2:
				label = self.drawMessage( "Reliability : " +  str( self.__bag.object[ "reliability" ] ), 50, ( height / 4 ) + 300, False, 25, "blue" )
			else:
				label = self.drawMessage( "Reliability : " + str( self.__bag.object[ "reliability" ] ), 50, ( height / 4 ) + 300, False, 25, "white" )

	def score( self ):
		width = self.__bag.screen.get_rect().width
		height = self.__bag.screen.get_rect().height

		## calculate percent
		won = ( int( self.__user.attrib[ "won" ] ) / int( self.__user.attrib[ "total" ] ) ) * 100
		tied = ( int( self.__user.attrib[ "tied" ] ) / int( self.__user.attrib[ "total" ] ) ) * 100
		loose = ( int( self.__user.attrib[ "loose" ] ) / int( self.__user.attrib[ "total" ] ) ) * 100

		## Draw rect and fill the background
		self.drawRect( 0, 0, width, height, "grey" )

		# Write the title
		self.drawMessage( str( self.__user.attrib[ "name" ] ) + ", are you smart ?", ( width / 2 ), ( height / 9 ), True, self.__font[ "size" ], "white" )
		self.drawMessage( "(apparently not...)", ( width / 2 ), ( height / 9 ) + 40, True, 25, "white", False )

		for child in self.__user:
			if child.tag == "stats":
				count = 0
				for stepChild in child:
					self.drawMessage( stepChild.text + ": " + str( stepChild.attrib[ "value" ] ), ( width / 2 ), ( height / 3 ) + count, True, 30, stepChild.attrib[ "color" ], bool( stepChild.attrib[ "bold" ] ) )
					count += 35

		## Draw charts
		self.drawRect( 0, height - 60, width * ( won / 100 ), 80, "yellow" )
		self.drawMessage( "Won" + " (" + str( round( won, 1 ) ) + "%)", ( width * ( won / 100 ) ) / 2, height - 30, True, 18, "white", True )
		self.drawRect( width * ( won / 100 ), height - 60, width * ( tied / 100 ), 80, "blue" )
		self.drawMessage( "Tied" + " (" + str( round( tied, 1 ) ) + "%)", width * ( won / 100 ) + ( (  width * ( tied / 100 ) ) / 2 ), height - 30, True, 18, "white", True )
		self.drawRect( width * ( won / 100 ) + width * ( tied / 100 ), height - 60, width * ( loose / 100 ), 80, "red" )
		self.drawMessage( "Loose" + " (" + str( round( loose, 1 ) ) + "%)", width * ( won / 100 ) + width * ( tied / 100 ) + ( width * ( loose / 100 ) / 2 ) , height - 30, True, 18, "white", True )

	def wait( self ):
		## Draw rect and fill the background
		self.drawRect( 0, 0, self.__bag.screen.get_rect().width, self.__bag.screen.get_rect().height, "grey" )

		# Write a message
		self.drawMessage( "Please wait for other players...", ( self.__bag.screen.get_rect().width / 2 ), ( self.__bag.screen.get_rect().height / 2 ) - ( self.__bag.screen.get_rect().height / 9 ), True, self.__font[ "size" ], "white" )

		## Progression bar
		height = 20
		y = self.__bag.screen.get_rect().height / 1.5
		self.drawRect( self.__waitBar[ "x" ], y, self.__waitBar[ "width" ], height, "yellow" )

		## Animation
		self.__waitBar[ "x" ] += self.__waitBar[ "ratioX" ]
		if ( self.__waitBar[ "x" ] > ( self.__bag.screen.get_rect().width - self.__waitBar[ "width" ] ) ):
			self.__waitBar[ "ratioX" ] *= -1
		elif ( self.__waitBar[ "x" ] <= 0 ):
			self.__waitBar[ "ratioX" ] *= -1

	def objectInformations( self ):
		## Mouse position
		mouse = pygame.mouse.get_pos()

		width = self.__bag.screen.get_rect().width / 6
		height = self.__bag.screen.get_rect().height / 6

		for key, object in enumerate( self.__bag.objects ):
			if "x" in object:
				if ( ( mouse[ 0 ] >= object[ "x" ] and mouse[ 0 ] < ( object[ "x" ] + object[ "width" ] )  ) and ( mouse[ 1 ] >= object[ "y" ] and mouse[ 1 ] < ( object[ "y" ] + object[ "height" ] )  ) ):
					## Draw rect
					x = mouse[ 0 ]
					y = mouse[ 1 ]
					if ( x + width > self.__bag.screen.get_rect().width ):
						x = mouse[ 0 ] - width

					## Draw rect
					rect = self.drawRect( x, y, width, height, "white" )

					## Draw message
					self.drawMessage( "Strength : " + str( object[ "strength" ] ), x + ( width / 2 ), y + 20, True, 20, "grey" )
					self.drawMessage( "Defense : " + str( object[ "defense" ] ), x + ( width / 2 ), y + ( height / 2 ), True, 20, "grey" )
					self.drawMessage( "Reliability : " + str( object[ "reliability" ] ), x + ( width / 2 ), y + height - 20, True, 20, "grey" )


	def objects( self ):
		## Draw objects
		object = self.drawObjects( "All objects available", False )

		## Show informations about object
		self.objectInformations()

	def choosing( self ):
		## Draw objects
		self.drawObjects( "Choose your weapon", True )

		if self.__selectedObject != None and self.__bag.actionNetwork == net.LISTEN:
			self.__bag.actionNetwork = net.SEND
			self.__bag.messageNetwork = { "state": 3, "id": self.__selectedObject  }
			self.reinit()

		## Show informations about object
		self.objectInformations()