import os, sys
import pygame
import helpers
from pygame.locals import *


if not pygame.font: print( 'Warning, fonts disabled' )
if not pygame.mixer: print( 'Warning, sound disabled' )

class Client( object ):
	## The Main PyMan Class - This class handles the main initialization and creating of the Game.

	## variables
	__width = 640
	__height = 480
	__screen = None
	__network = None
    
	def __init__( self ):

		## Initialize PyGame
		pygame.init()

		## Initialize network
		self.__network = helpers.Network()
		self.__network.connect()


		## Create the Screen
		self.__screen = pygame.display.set_mode( ( self.__width, self.__height ) )

	def run( self ):
		## This is the main loop of the game
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
