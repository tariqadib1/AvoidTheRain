import pygame, random, threading

LEFT = 'LEFT'
RIGHT = 'RIGHT'
DOWN = 'DOWN'
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
playerLength = 30
playerWidth = 2
rainSize = [1,1]

def isPointInsideRect(x, y, rect):
	if (x > rect.left) and (x < rect.right) and (y > rect.top) and (y < rect.bottom):
		return True

def isCollision(drop,playerTab):
	if ((isPointInsideRect(drop.left, drop.top, playerTab)) or (isPointInsideRect(drop.left, drop.bottom, playerTab)) or (isPointInsideRect(drop.right, drop.top, playerTab)) or (isPointInsideRect(drop.right, drop.bottom, playerTab))):
		return True
	return False

def GameOver(killCount):
	font = pygame.font.Font('Calibri.ttf', 32)
	text = font.render("Game Over", True, RED, BLACK)
	textRect = text.get_rect() 
	textRect.center = (300,200)
	screen.blit(text, textRect)
	
	font = pygame.font.Font('Calibri.ttf', 30)
	text = font.render("Your Score = {}".format(killCount), True, RED, BLACK)
	textRect = text.get_rect() 
	textRect.center = (300,250)
	screen.blit(text, textRect)
	
	font = pygame.font.Font('Calibri.ttf', 28)
	text = font.render("Press (R) to Rest", True, RED, BLACK)
	textRect = text.get_rect() 
	textRect.center = (300,300)
	screen.blit(text, textRect)
	return True
	
def drawGame(player,rain,isGameOver):
	global screen,killCount,playerLength
	pSurface = pygame.Surface((playerLength,playerWidth))
	pSurface.fill(RED)
	screen.blit(pSurface,player)
	collisionDetected = False
	nextRain = []
	
	for drop in rain:
		dSurface = pygame.Surface(rainSize)
		dSurface.fill(WHITE)
		screen.blit(dSurface,drop)
		if drop[1] < 400:
			nextRain.append((drop[0],drop[1]+1))
		else:
			if not isGameOver:
				killCount += 1
			if killCount %50 == 0:
				print(killCount)
		if not collisionDetected:
			collisionDetected = isCollision(pygame.Rect(drop[0],drop[1],rainSize[0],rainSize[1]), pygame.Rect(player[0],player[1],playerLength,playerWidth))
	
	return nextRain, collisionDetected

def movePlayer(side):
	global player
	if side == LEFT:
		player[0] -= 20
	if side == RIGHT:
		player[0] += 20
	if player[0]<10:
		player[0]=10
	if player[0]>590:
		player[0]=590

def NewRainDrop():
	global rain
	x,y = random.randint(1,599),random.randint(1,199)
	for drops in rain:
		if x >= drops[0] and x <= drops[0]+rainSize[0]:
			return
	rain.append((x,y))
	
def main():
	global player,rain,killCount,screen,playerLength,rainDropFrequency
	
	pygame.init()
	pygame.display.set_caption('Avoid Rain')
	screen = pygame.display.set_mode((600,400))
	clock = pygame.time.Clock()
	
	difficultyControl = 0
	isGameOver=False
	killCount = 1
	rainDropFrequency = 400
	player = [random.randint(1,570),370]
	rain = []
	
	ADDRAINDROP = pygame.USEREVENT + 1
	pygame.time.set_timer(ADDRAINDROP, rainDropFrequency)
	
	while True:
		screen.fill(BLACK)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				print(killCount)
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					print(killCount)
					pygame.quit()
				if event.key == pygame.K_r:
					killCount = 0
					isGameOver = False
					rainDropFrequency = 200
					rain.clear()	
					screen.fill(WHITE)
					#playerLength = 10
			if not isGameOver and event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					movePlayer(LEFT)
				if event.key == pygame.K_RIGHT:
					movePlayer(RIGHT)
			if event.type == ADDRAINDROP:
				# ~ newThread = threading.Thread(target=NewRainDrop, args=())
				# ~ newThread.start()
				NewRainDrop()
					
		rain, collisionDetected = drawGame(player,rain,isGameOver)
		
		# ~ newThread = threading.Thread(target=drawGame, args=(player,rain,isGameOver))
		# ~ newThread.start()
		# ~ collisionDetected = newThread.join()
		
		# ~ print(collisionDetected)
		# ~ print(killCount)
		if collisionDetected or isGameOver:
			isGameOver=GameOver(killCount)
		
		if killCount % 50 == 0 and difficultyControl!=killCount:
			difficultyControl=killCount
			rainDropFrequency -= 20
			#playerLength += 5
		
		pygame.display.update()
		clock.tick(60)

if __name__ == '__main__':
	main()
