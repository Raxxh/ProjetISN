import pygame
import Tile
import sys
import random

def coord2px(x, y):
	return (353+155*x,16+155*y)

def display(fallTime = 0):
	screen.blit(backgroundImg,(0,0))
	x = 0
	while x < 4 :
		y = 0
		while y < 4 :
			if tiles[x][y] != None :
				tiles[x][y].display(screen, coord2px(x,y), fallTime) # need to calc real X and Y
			y += 1
		x += 1

	if won():
		screen.blit(wonImg, (0,0))

	displayText(str(score[0]), (1025,200))
	pygame.display.flip()

def displayText(text, pos):
	label = myfont.render(text, 1, (0,0,0))
	screen.blit(label, pos)

def won():
	for x in range(0,4):
		for y in range(0,4):
			if (tiles[x][y] != None):
				if (tiles[x][y].getValue() >= 2048):
					return True
	return False

def loose():
	print("LOST")
	display()
	screen.blit(pygame.image.load("../img/lost.png"), (0,0))
	pygame.display.flip()
	# TODO : aff les scores
	while True:
		event = pygame.event.poll()
		if event.type == pygame.QUIT:
			sys.exit()

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

	for x in range(0,4):
		for y in range(0,4):
			if ( tiles[x][y] == None):
				return
	# GRILLE COMPLETE, CHECK LOOSE
	for x in range(0,3):
		for y in range(0,4):
			if (tiles[x][y].getValue() == tiles[x+1][y].getValue()):
				return
	for x in range(0,4):
		for y in range(0,3):
			if (tiles[x][y].getValue() == tiles[x][y+1].getValue()):
				return
	loose()

#--- Fall functions  TODO yanis/maxence
"""
Fonctionnement : Pour chaque tuile, calcule l'écart entre la pos finale et initiale
et la fait tomber à une certaine vitesse pour que tous les tuiles arrivent
en même temps.
Puis, on affiche directement la nouvelle grille
/!\
Galère, on les fait tous tomber à la même vitesse avec des check
d'arret individuel
En fait nn c'ests chiant aussi
re à la méthode prévue
"""
def getFallDistance(arg):
	result = 0
	last = None
	for tile in arg:
		if (tile == None):
			result += 1
		elif (last == None):
			last = tile
		elif (tile.getValue() == last.getValue()):
			result += 1
			last = None
		else:
			last = tile
	return result

def getTileList():
	result = []
	for x in range(0,4):
		for y in range(0,4):
			if tiles[x][y] != None:
				result.append(tiles[x][y])
	return result

def setLastGrid(grid):
	for x in range(0, 4):
		for y in range(0,4):
			lastGrid[x][y] = grid[x][y]

def setGrid(grid, pos, t):
	grid[pos[0]][pos[1]] = t

def getGrid(grid, pos):
	return grid[pos[0]][pos[1]]

def setTiles(grid):
	x = 0
	while x < 4:
		y = 0
		while y < 4:
			tiles[x][y] = grid[x][y]
			y += 1
		x += 1

def fall(direction):
	speed = 25
	tilesOnWay = []
	newList = [[None for x in range(4)] for y in range(4)]
	liste = getTileList()
	newScore = score[0]

	i = 0
	x = 0
	
	if direction == "right":
		for x in range(0,4):
			for y in range(0,4):
				if tiles[x][y] == None:
					continue
				tilesOnWay = []
				for i in range(x,4):
					tilesOnWay.append(tiles[i][y])

				tiles[x][y].finalPos((x + getFallDistance(tilesOnWay), y))
				tiles[x][y].setSpeed((getFallDistance(tilesOnWay), 0))

	if direction == "down":
		for x in range(0,4):
			for y in range(0,4):
				if tiles[x][y] == None:
					continue
				tilesOnWay = []
				for i in range(y,4):
					tilesOnWay.append(tiles[x][i])

				tiles[x][y].finalPos((x, y + getFallDistance(tilesOnWay)))
				tiles[x][y].setSpeed((0, getFallDistance(tilesOnWay)))

	if direction == "left":
		for x in range(3,-1,-1):
			for y in range(0,4):
				if tiles[x][y] == None:
					continue
				tilesOnWay = []
				for i in range(0,x+1):
					tilesOnWay.append(tiles[i][y])

				tiles[x][y].finalPos((x - getFallDistance(tilesOnWay), y))
				tiles[x][y].setSpeed((-getFallDistance(tilesOnWay), 0))

	if direction == "up":
		for x in range(0,4):
			for y in range(3,-1,-1):
				if tiles[x][y] == None:
					continue
				tilesOnWay = []
				for i in range(0,y+1):
					tilesOnWay.append(tiles[x][i])

				tiles[x][y].finalPos((x, y - getFallDistance(tilesOnWay)))
				tiles[x][y].setSpeed((0, -getFallDistance(tilesOnWay)))

	lastScore[0] = score[0]
	for t in liste:
		if (getGrid(newList, t.finalPos()) != None):
			if (getGrid(newList, t.finalPos()).getValue() == t.getValue()):
				setGrid(newList, t.finalPos(), Tile.Tile(t.getValue() * 2))
				newScore += t.getValue() * 2
			else:
				continue
		else:
			setGrid(newList, t.finalPos(), t)

	if ( newList == tiles): # mouvement interdit
		return False

	setLastGrid(tiles)

	time = 1
	while time < 155 : 
		display(time)
		time += speed


	setTiles(newList)
	score[0] = newScore
	return True


def right():
	return fall("right")
def left():
	return fall("left")
def up():
	return fall("up")
def down():
	return fall("down")

def NewGame():
	setTiles([[None for x in range(4)] for y in range(4)])
	score = 0
	return True
	
def Back():
	setTiles(lastGrid)
	score[0] = lastScore[0]
	display()
	return False

def play():
	keyEvents = {
				 	273:up,
					274:down,
					276:left,
					275:right,
					13:NewGame,
					8:Back
				}
	while True:
		event = pygame.event.poll()
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key in keyEvents:
				return keyEvents[event.key]()
				

################### DEBUT #######################

pygame.init()
width, height = 1152,648

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('2048')
myfont = pygame.font.SysFont("monospace", 30)

wonImg = pygame.image.load("../img/won.png")
backgroundImg = pygame.image.load("../img/background.png")
tiles = [[None for x in range(4)] for y in range(4)]
lastGrid = [[None for x in range(4)] for y in range(4)]
score = [0]
lastScore = [0]

if (not pygame.display):
	print("Error during window creation")

# MAIN LOOP #
while True :
	newRandomTile()
	display()
	while not play():
		pass