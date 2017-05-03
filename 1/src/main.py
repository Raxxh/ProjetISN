import pygame
import Tile
import sys
import random

def display(fallTime = 0):
	# needs test but should work
	screen.blit(backgroundImg,(0,0))
	x = 0
	while x < 4 :
		y = 0
		while y < 4 :
			if tiles[x][y] != None :
				tiles[x][y].display(screen, tiles[x][y].coord2px(x,y)) # need to calc real X and Y
			y += 1
		x += 1

	pygame.display.flip()

def won():
	#TODO maxence
	return

def loose():
	#TODO
	return

def fusion(t1, t2):
	return None

def newRandomTile():
	# random.randrange(0,4) => 0,1,2,3
	# TODO : check if grid is full
	x = random.randrange(0,4)
	y = random.randrange(0,4)
	while tiles[x][y] != None :
		x = random.randrange(0,4)
		y = random.randrange(0,4)
	if random.randrange(0,10) == 1:
		tiles[x][y] = Tile.Tile(4)
	else :
		tiles[x][y] = Tile.Tile(2)

def debugGrid():
	debug = ""
	y = 0
	while y < 4 :
		x = 0
		s=""
		while x < 4 :
			s += " "
			debug += "y: " + str(y) + ", x: " + str(x) + " :" + str(tiles[x][y])
			if tiles[x][y] != None :
				s += str(tiles[x][y].getValue())
			else:
				s += "n"
			x += 1
			debug+="\n"
		print(s)
		y += 1
	print("======")
	print(debug)

#--- Fall functions  TODO yanis/maxence
"""
Fonctionnement : Pour chaque tile, calcule l'écart entre la pos finale et initiale
et la fait tomber à une certaine vitesse pour que touts les tiles arrivent
en même temps.
Puis, on affiche directement la nouvelle grille
/!\
Galère, on les fait tous tomber à la même vitesse avec des check
d'arret individuel
En fait nn c'ests chiant aussi
re à la méthode prévue
"""
def getFallDistance(arg): # a tester rapid, devrait être bon
	last = None
	justFused = False
	result = 0
	for tile in arg :
		if (tile != last) and (tile != None) and (not justFused):
			result += 1
			justFused = True
		else:
			justFused = False
		last = tile 
	return result

def checkTileStop(coord, direction):
	# check if the tile should stop falling
	tileToCheck = None
	if ( direction == "right"):
		tileToCheck = tiles[x + 1][y]
	if ( direction == "left"):
		tileToCheck = tiles[x - 1][y]
	if ( direction == "up"):
		tileToCheck = tiles[x][y + 1]
	if ( direction == "down"):
		tileToCheck = tiles[x][y - 1]

	if( tileToCheck == None):
		return False
	return tiles[x][y].getValue() != tileToCheck.getValue()

def updateGridWhileFalling(before, after):
	#TODO , px2coord a tester avant !!
	return

def	checkFusion(coord, direction):
	return False # TODO

def fall(direction):
	#--- gen de la vitesse individuel
	"""	speed = 1
	tileOnWay = []
	i = 0
	x = 0
	while x < 4 : # revoir la logique, 2 diff boucles, une x : doite/gauche, un y : haut/bas
		y = 0
		while y < 4 : 
			if tiles[x][y] != None :
				if (direction == "right"): # FALLING RIGHT
					i = x + 1
					while i < 3 :
						if tiles[x+i][y] != None :
							tileOnWay.append(tiles[x+i][y])
							i += 1
					dirVect = (speed*getFallDistance(tileOnWay),0)

				if (direction == "left"): # FALLING LEFT
					i = x - 1
					while i >= 0 :
						if tiles[x-i][y] != None :
							tileOnWay.append(tiles[x-i][y])
						i -= 1
					dirVect = (-speed*getFallDistance(tileOnWay),0)

				if (direction == "down"): # FALLING DOWN
					i = y + 1
					while i < 3 :
						if tiles[x][y+i] != None :
							tileOnWay.append(tiles[x][y+i])
						i += 1
					dirVect = (0,speed*getFallDistance(tileOnWay))

				if (direction == "up"): # FALLING LEFT
					i = y - 1
					while i >= 0 :
						if tiles[x][y-i] != None :
							tileOnWay.append(tiles[x][y-i])
						i -= 1
					dirVect = (0,-speed*getFallDistance(tileOnWay))

				tiles[x][y].setFallPosMod(dirVect)
			y += 1
		x += 1 # NEED TESTS !!!!! 

	time = 0 # TODO : use real system time
	while time < 1/speed : # 1/speed ??
		display(time)
		time += 1
	"""

	#--- VITESSE CONSTANTE
	#todo
	
	for a in tiles:
		for b in a:
			if (b != None):
				b.isFalling(True)
	speed = 1

	if (direction == "right"):
		x = 3
		y = 0
		while (y < 4):
			while (x >= 0 ):
				if (tiles[x][y] == None or not tiles[x][y].isFalling()):
					continue
				if (checkTileStop(tiles[x][y].coord2px(x,y), "right")):
					tiles[x][y].isFalling(False)
				else:
					tiles[x][y].setFallPosModRelative((1,0))
				checkFusion(tiles[x,y].coord2px(x,y), "right")
				updateGridWhileFalling((x,y), tiles[x][y].coord2px(x,y))
				x -= 1
			y += 1
	return


def right(): # fall on right
	fall("right")
def left(): # fall on left
	fall("left")
def up(): # fall on top
	fall("up")
def down(): # fall on bottom
	fall("down")

def play():
	keyEvents = {
				 	273:up,
					274:down,
					276:left,
					275:right,
				}
	while True:
		event = pygame.event.poll()
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key in keyEvents:
				keyEvents[event.key]()
				return

################### DEBUT #######################

pygame.init()
width, height = 1152,648
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('2048')

backgroundImg = pygame.image.load("../img/background.png")
tiles = [[None for x in range(4)] for y in range(4)]

if (not pygame.display):
	print("Error during window creation")

# MAIN LOOP #
while not won() :
	newRandomTile()
	display()
	play()