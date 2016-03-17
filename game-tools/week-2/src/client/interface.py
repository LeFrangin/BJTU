import os, sys
import pygame
import helpers
import menu
from config import Action, State
from pygame.locals import *

if not pygame.font: print( 'Warning, fonts disabled' )
if not pygame.mixer: print( 'Warning, sound disabled' )

class Client( object ):
	## The Main PyMan Class - This class handles the main initialization and creating of the Game.

	## variables
	__screen = None
	__network = None
	__clock = None
	__menu = None
	__state = State.MENU
	__action = None
    
	def __init__( self ):

		## Initialize PyGame
		pygame.init()
		pygame.display.set_caption( "Toto" )
		self.__clock = pygame.time.Clock()

		## Initialize network
		self.__network = helpers.Network()
		# self.__network.connect()

		## Create the Screen
		self.__screen = pygame.display.set_mode( ( 1080, 720 ), RESIZABLE )

		## Initialize network
		self.__menu = menu.Client( self.__screen )

	def run( self ):
		## This is the main loop of the game
		
		while 1:
			self.__clock.tick( 50 );
			for event in pygame.event.get():
				print( pygame.event.event_name( event.type ) )
				## catch event
				if event.type == pygame.QUIT or ( event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE ):
					self.quit()
					break
				elif event.type == pygame.VIDEORESIZE:
					self.__screen = pygame.display.set_mode( event.size, RESIZABLE )
				
				## catch keyboard
				if event.type == pygame.KEYDOWN:
					print( event.key )

			if self.__state == State.MENU:
				self.__action = self.__menu.display()

			## Check if we need to quit the game
			if self.__action == Action.QUIT:
				self.quit()
				break

			pygame.display.flip()

	def quit( self ):
		sys.exit()
		