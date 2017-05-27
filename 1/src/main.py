# Imports
import pygame 	# graphismes
import Tile 	# tuiles
import sys 		# sys.exit()
import random 	# gen de nouvelles tuiles
import time 	# temps

def coord2px(x, y):
	""" Converti les coordonnées du tableau en pixel """
	return (353+155*x,16+155*y)

def getTimeStr():
	""" Retourne le temps a afficher """
	timeNow = time.time() - GameBeginTime[0]
	
	hours = int(timeNow // 3600)
	mint = int(timeNow // 60)
	sec = int(timeNow % 60)

	if sec < 10:
		sec = '0' + str(sec)
	if mint < 10:
		mint = '0' + str(mint)

	return str(hours) + ":" + str(mint) + ":" + str(sec)

def display(fallTime = 0):
	""" Affiche le tout en fonction du temps de chute """
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

	# Score et Temps
	displayText(str(score[0]), (1025,200))
	displayText(getTimeStr(), (1000, 300))
	pygame.display.flip()

def displayText(text, pos):
	""" affiche du texte au coordonnées indiquée """
	label = myfont.render(text, 1, (0,0,0))
	screen.blit(label, pos)

def won():
	""" Definit si le joueur a gagné ou non """
	for tile in getTileList():
		if (tile.getValue() >= 2048):
			return True
	return False

def loose():
	""" Affiche l'écran de fin """
	display()
	screen.blit(pygame.image.load("../img/lost.png"), (0,0))
	pygame.display.flip()
	while True:
		event = pygame.event.poll()
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == 8:
				return Back()

def newRandomTile():
	""" Fait apparaitre une nouvelle tuile
	et check si on perd """
	# random.randrange(0,4) => 0,1,2,3
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

def getFallDistance(arg):
	""" Retourne la distance de chute
	en fonction des tuiles sur la route """
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
	""" Retourne une liste des tuiles
	dans une liste unidimentionelle """
	result = []
	for x in range(0,4):
		for y in range(0,4):
			if tiles[x][y] != None:
				result.append(tiles[x][y])
	return result

def setLastGrid(grid):
	""" sauvegarde la grille indiquée
	comme la grille du dernier tour """
	for x in range(0, 4):
		for y in range(0,4):
			lastGrid[x][y] = grid[x][y]

def setGrid(grid, pos, t):
	""" Remplace l'élément de la grille indiquée
	à l'index indiquée par l'élément indiqué """
	grid[pos[0]][pos[1]] = t

def getGrid(grid, pos):
	""" retourne la valeure dans l'indexe indiqué
	de la grille indiquée """
	return grid[pos[0]][pos[1]]

def setTiles(grid):
	""" Remplace la grille principale 
	par la grille indiquée """
	x = 0
	while x < 4:
		y = 0
		while y < 4:
			tiles[x][y] = grid[x][y]
			y += 1
		x += 1

def fall(direction):
	""" Fais tomber les tuiles 
	dans la direction indiquée """
	speed = 25
	tilesOnWay = []
	newList = [[None for x in range(4)] for y in range(4)]
	liste = getTileList()
	newScore = score[0]

	i = 0
	x = 0
	
	""" Definission d'une vitesse et de la position finale
 	des tuiles individuellement """

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

	""" Definition de la nouvelle grille ( après le mouvement ) """

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

	# Animation
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
	""" Réinitialise la partie """
	setTiles([[None for x in range(4)] for y in range(4)])
	score = 0
	GameBeginTime[0] = time.time()
	return True
	
def Back():
	""" Retour arrière """
	setTiles(lastGrid)
	score[0] = lastScore[0]
	display()
	return False

def play():
	""" Gère les évenements """
	keyEvents = {
				 	273:up,
					274:down,
					276:left,
					275:right,
					13:NewGame,
					8:Back
				}
	while True:
		display()
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

GameBeginTime = [time.time()]

if (not pygame.display):
	print("Error during window creation")

# MAIN LOOP #
while True :
	newRandomTile()
	display()
	while not play():
		pass