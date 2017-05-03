import pygame

class Tile():
	def __init__(self, size):
		self.size = size
		self.texture = pygame.image.load("../img/Tiles/"+str(size)+".png")
		self.fallPosMod = (0,0)

	def display(self, screen, pos):
		screen.blit(self.texture, pos)

	def getValue(self):
		return self.size

	def fallTick(self, nbOfCase, direction, time):
		speedByCase = 1 # A DEFINIR
		self.fallPosMod = direction*speedByCase*nbOfCase*time

	def getFallPosMod(self):
		return self.fallPosMod

	def setFallPosMod(self, arg):
		self.fallPosMod = arg

	def setFallPosModRelative(self, arg):
		self.fallPosMod += arg

	def coord2px(self, x, y):
		return (353+155*x,16+155*y) + self.fallPosMod # to update

	def px2coord(self, x, y): # NEED TESTS !!!!!
		return (((x,y)-self.fallPosMod)-(353,16))/(155,155)

	def isFalling(self, value = None):
		if ( value != None):
			self.isFalling = value
		return self.isFalling