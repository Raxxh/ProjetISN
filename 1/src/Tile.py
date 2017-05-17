import pygame

class Tile():
	def __init__(self, size):
		self.size = size
		self.texture = pygame.image.load("../img/Tiles/"+str(size)+".png")
		self.speed = (0,0)


	def display(self, screen, pos, fallTime):
		screen.blit(self.texture, tuple(map(sum,zip(pos, tuple([fallTime*x for x in self.speed])))))

	def getValue(self):
		return self.size

	def setSpeed(self, arg):
		self.speed = arg

	def finalPos(self, value = None):
		if ( value != None):
			self.finalpos = value
		return self.finalpos
