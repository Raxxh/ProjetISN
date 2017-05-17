import pygame
import Tile

class Grille():
	def __init__(self):
		self.background = pygame.image.load("../img/background.png")
		self.tiles = [[None] *4] * 4

	def display(self, screen):
		# needs test but should work
		screen.blit(self.background,(0,0))
		x = 0
		while x < 4 :
			y = 0
			while y < 4 :
				if self.tiles[x][y] != None :
					self.tiles[x][y].display((x,y))
				y += 1
			x += 1

		pygame.display.flip()

	def setTile(pos, tile):
		#TODO maxence
		return

	def hightestTile(self):
		#TODO maxence
		return 0