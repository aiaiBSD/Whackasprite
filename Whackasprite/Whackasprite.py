import random, sys, time, pygame
from pygame.locals import *
from pygame.font import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARKGRAY = (47, 79, 79)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
BLUE = (0, 0, 255)


#-------------------------------
class Fizzy (pygame.sprite.Sprite):

    def __init__(self, xPos, yPos):
        super().__init__()
        self.image = pygame.image.load("fizzy.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.x = xPos
        self.y = yPos
        self.rect.topleft = (xPos, yPos)


    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

#---------------------------------

def generateRevealedSpritesData(val):
    revealedSprites = []
    for i in range(BOARDWIDTH):
        revealedSprites.append([val] * BOARDHEIGHT)
    return revealedSprites

#---------------------------------

def drawScreen(screen, time, fizzy, revealed, hits, go):
    screen.fill(WHITE)
    timeIm = font.render(str(time), True, BLACK)
    screen.blit(timeIm, (10, 10))
    hitIm = font.render('Hits = ' + str(hits), True, BLACK)
    screen.blit(hitIm, (820, 10))
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            if revealedSprites[boxx][boxy]:
                fizzy[boxx][boxy].draw(screen)
    pygame.display.update()
    if go == False:
        youLose = font.render('You Lose!', True, BLACK)
        screen.blit(youLose, (400, 10))

#-----------------------------------

def checkLose(revealed):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if revealed[x][y] == False:
                return False
    return True

#----------- main ----------------

BOARDWIDTH = 6
BOARDHEIGHT = 6
pygame.init()
screen = pygame.display.set_mode([960, 720])
screen.fill(WHITE)
pygame.display.set_caption('Whackasprite')

scrWidth, scrHeight = screen.get_size()

font = pygame.font.Font(None, 40)

fizzy = []
xPixel = 115
for x in range(BOARDWIDTH):
    column = []
    yPixel = 90
    for y in range(BOARDHEIGHT):
        column.append(Fizzy(xPixel, yPixel))
        yPixel += 90
    fizzy.append(column)
    xPixel += 120

hits = 0
mousex = 0
mousey = 0

revealedSprites = generateRevealedSpritesData(False)

clock = pygame.time.Clock()

running = True
while running:
    clock.tick(30)
    mouseClicked = False
    go = True
    if checkLose(revealedSprites):
        go = False

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        if event.type == MOUSEMOTION:
            mousex, mousey = event.pos

        if event.type == MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            mouseClicked = True

    if mouseClicked == True and go:
        for boxx in range(BOARDWIDTH):
            for boxy in range(BOARDHEIGHT):
                if revealedSprites[boxx][boxy] and mousex >= (fizzy[boxx][boxy].getX() + 24) and mousex <= (fizzy[boxx][boxy].getX() + 90 - 25) and mousey >= (fizzy[boxx][boxy].getY() + 6) and mousey <= (fizzy[boxx][boxy].getY() + 90 - 7):
                    hits += 1
                    revealedSprites[boxx][boxy] = False

    spawnRate = int(hits / 10)
    if spawnRate == 0 and go:
        tempTime = pygame.time.get_ticks()
        if tempTime % 100 == 0:
            go = True
            posOne = -1
            posTwo = -2
            while go:
                posOne = random.randint(0, 5)
                posTwo = random.randint(0, 5)
                if revealedSprites[posOne][posTwo] == False:
                    go = False
            revealedSprites[posOne][posTwo] = True
    if spawnRate > 0 and go:
        tempTime = pygame.time.get_ticks()
        factor = int(100/spawnRate)
        if tempTime % factor == 0:
            go = True
            posOne = -1
            posTwo = -2
            while go:
                posOne = random.randint(0, 5)
                posTwo = random.randint(0, 5)
                if revealedSprites[posOne][posTwo] == False:
                    go = False
            revealedSprites[posOne][posTwo] = True

    screen.fill(WHITE)
    time = int(pygame.time.get_ticks()/1000)
    drawScreen(screen, time, fizzy, revealedSprites, hits, go)

pygame.quit()


