import os, sys
import pygame
import helpers
import menu
import engine
from config import State, Result
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
	__key = None
	__game = None
	__state = State.MENU
    
	def __init__( self ):

		## Initialize PyGame
		pygame.init()
		pygame.mixer.init()
		pygame.display.set_caption( "Toto" )
		self.__clock = pygame.time.Clock()

		## Initialize network
		self.__network = helpers.Network()
		# self.__network.connect()

		## Create the Screen
		self.__screen = pygame.display.set_mode( ( 1080, 720 ), RESIZABLE )

		## Initialize helpers
		self.__menu = menu.Client( self.__screen )
		self.__game = engine.Game( self.__screen )

	def run( self ):
		## This is the main loop of the game
		
		while 1:
			self.__clock.tick( 60 );
			for event in pygame.event.get():
				# print( pygame.event.event_name( event.type ) )
				## catch event
				if event.type == pygame.QUIT:
					self.quit()
					break
				elif event.type == pygame.VIDEORESIZE:
					self.__screen = pygame.display.set_mode( event.size, RESIZABLE )
				
				## catch keyboard
				if event.type == pygame.KEYDOWN:
					self.__key = event.key
					print(event.key)

			if self.__state == State.MENU or self.__key == pygame.K_ESCAPE:
				self.__state = self.__menu.display()
				self.__key = None

			if self.__state == State.PENDING:
				self.__game.wait()
			elif self.__state == State.WAITING:
				self.__game.wait()
			elif self.__state == State.CHOOSING:
				self.__game.objects( True )
			elif self.__state == State.RESULT:
				self.__game.result( Result.WIN )
			elif self.__state == State.CHOOSING:
				self.__game.objects( True )
			elif self.__state == State.OBJECTS:
				self.__game.objects( False )
			elif self.__state == State.QUIT:
				self.quit()
				break

			pygame.display.flip()

	def game( self ):
		pass

	def quit( self ):
		pygame.quit()
		sys.exit()
		