import os, sys
import pygame
import helpers
import menu
import engine
from config import Status, Result, Network as net
from pygame.locals import *
from threading import Thread

if not pygame.font: print( 'Warning, fonts disabled' )
if not pygame.mixer: print( 'Warning, sound disabled' )

class Bag( object ):
	## The Bag Class - This class handles all variables and states of the game between threads.

	## variables
	actionNetwork = net.CONNECT
	messageNetwork = ""
	responseNetwork = ""
	statusNetwork = net.OFFLINE
	status = Status.MENU
	result = None
	key = None
	screen = None
	clock = pygame.time.Clock()

	def __init__( self ):
		pass

class Client( object ):
	## The Main PyMan Class - This class handles the main initialization and creating of the Game.

	## variables
	__bag = Bag
	__threads = {}
	__clock = None
	__menu = None
	__game = None
	__functions = None
    
	def __init__( self ):

		## Initialize PyGame
		pygame.init()
		pygame.mixer.init()
		pygame.display.set_caption( "Toto" )
		self.__clock = pygame.time.Clock()
		pygame.mouse.set_cursor( *pygame.cursors.tri_left )

		## Create the Screen
		self.__bag.screen = pygame.display.set_mode( ( 1080, 720 ), RESIZABLE )

		## Initialize threads
		# Network
		self.__threads[ "network" ] = helpers.Network( self.__bag )
		self.__threads[ "network" ].start()
		# Menu
		self.__threads[ "menu" ] = menu.Client( self.__bag )
		self.__threads[ "menu" ].start()

		## Create engine
		self.__game = engine.Game( self.__bag )

		## Dictionnary of functions
		self.__functions = {
			Status.WAITING: self.__game.wait,
			Status.CHOOSING: self.__game.choosing,
			Status.OBJECTS: self.__game.objects,
			Status.RESULT: self.__game.result,
			Status.SCORE: self.__game.score,
			Status.RULE: self.__game.rule,
		}

	def run( self ):
		## This is the main loop of the game
		
		while self.__bag.status != Status.QUIT:
			self.__clock.tick( 60 );
			for event in pygame.event.get():
				# print( pygame.event.event_name( event.type ) )
				## catch event
				if event.type == pygame.QUIT:
					self.quit()
				elif event.type == pygame.VIDEORESIZE:
					self.__bag.screen = pygame.display.set_mode( event.size, RESIZABLE )
				
				## catch keyboard
				if event.type == pygame.KEYDOWN:
					self.__bag.key = event.key
					print( event.key )

			if self.__bag.key == pygame.K_ESCAPE:
				self.__bag.key = None
				self.__bag.status = Status.MENU
				if ( self.__bag.statusNetwork == net.ONLINE ):
					self.__bag.actionNetwork = net.LISTEN
				else:
					self.__bag.actionNetwork = net.CONNECT
				self.__bag.messageNetwork = ""

			## Choose which function of the game engine to call
			if self.__bag.status in self.__functions:
				self.__functions[ self.__bag.status ]()

			pygame.display.flip()

		## End the programm	
		self.quit()

	def quit( self ):
		self.__bag.status = Status.QUIT
		for key, thread in self.__threads.items():
			thread.join()
		pygame.quit()
		sys.exit()
		