"""
Filename: slidergame.py
Interpreter: 2.7
Author: Tim Johnson
Description: A game built with pygame that involves the player solving puzzles by sliding the
                hero across a grid until it reaches the goal.
"""
import sys, pygame, math, pygame.mixer
pygame.init()

# Constants
GRID_SIZE = 25
ID_WALL             = 1
ID_LAVA             = 2
ID_GOAL             = 3
ID_ORANGE_BUTTON    = 4
ID_ORANGE_TILE_OFF  = 5
ID_TEAL_BUTTON      = 6
ID_TEAL_TILE_OFF    = 7
ID_BLUE_BUTTON      = 8
ID_BLUE_TILE_OFF    = 9
ID_PINK_TP          = 10
ID_PURPLE_TP        = 11
ID_ORANGE_TILE_ON   = 12
ID_TEAL_TILE_ON     = 13
ID_BLUE_TILE_ON     = 14
FINAL_LEVEL = 12

# Colors
backgroundClr = 0, 0, 0

# Sprites
gameArea = pygame.Surface((500, 500))
floorTile = pygame.Surface((20, 20))
wallTile = pygame.Surface((20, 20))
lavaTile = pygame.Surface((20, 20))
goalTile = pygame.Surface((20, 20))
switchTile1 = pygame.Surface((20, 20))
disappearingTile1a = pygame.Surface((20, 20))
disappearingTile1d = pygame.Surface((20, 20))
switchTile2 = pygame.Surface((20, 20))
disappearingTile2a = pygame.Surface((20, 20))
disappearingTile2d = pygame.Surface((20, 20))
switchTile3 = pygame.Surface((20, 20))
disappearingTile3a = pygame.Surface((20, 20))
disappearingTile3d = pygame.Surface((20, 20))
tpTile1 = pygame.Surface((20, 20))
tpTile2 = pygame.Surface((20, 20))
largeFont = pygame.font.SysFont('helvetica', 30)
hero = pygame.Surface((20, 20))

# Game Variables
screen = pygame.display.set_mode((500, 540))
levelGrid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
disappearingTilesOn = [True, True, True]
disappearingTilesInitState = [True, True, True]
tp1Locations = [(-1, -1), (-1, -1)]
tp2Locations = [(-1, -1), (-1, -1)]
heroPos = [-1, -1]
heroVel = [0, 0]
spawn = -1, -1
keysDown = [False] * 500
keysJustPressed = [False] * 500
currentLevel = 1
speed = 5
lvlTitle = ""

def init():
    """
    Initializes all sprites and the window
    :return: None
    """
    pygame.display.set_caption("Slider Game")

    borderColor = 84, 84, 69

    floorColor = 119, 119, 98
    floorTile.fill(borderColor)
    floorTile.fill(floorColor, pygame.Rect(1, 1, 18, 18))

    wallColor = 255, 255, 255
    wallTile.fill(borderColor)
    wallTile.fill(wallColor, pygame.Rect(1, 1, 18, 18))

    lavaColor = 237, 60, 21
    lavaTile.fill(lavaColor, pygame.Rect(0, 0, 20, 20))

    goalColor = 80, 244, 66
    goalTile.fill(borderColor)
    goalTile.fill(goalColor, pygame.Rect(1, 1, 18, 18))

    switchColor1a = 226, 180, 93
    switchColor1b = 244, 213, 154
    switchTile1.fill(switchColor1a, pygame.Rect(0, 0, 10, 10))
    switchTile1.fill(switchColor1b, pygame.Rect(10, 0, 10, 10))
    switchTile1.fill(switchColor1a, pygame.Rect(10, 10, 10, 10))
    switchTile1.fill(switchColor1b, pygame.Rect(0, 10, 10, 10))

    disappearingColor1a = 255, 182, 0
    disappearingTile1a.fill(borderColor)
    disappearingTile1a.fill(disappearingColor1a, pygame.Rect(1, 1, 18, 18))
    disappearingColor1d = 142, 101, 0
    disappearingTile1d.fill(borderColor)
    disappearingTile1d.fill(disappearingColor1d, pygame.Rect(1, 1, 18, 18))

    switchColor2a = 56, 202, 216
    switchColor2b = 146, 224, 232
    switchTile2.fill(switchColor2a, pygame.Rect(0, 0, 10, 10))
    switchTile2.fill(switchColor2b, pygame.Rect(10, 0, 10, 10))
    switchTile2.fill(switchColor2a, pygame.Rect(10, 10, 10, 10))
    switchTile2.fill(switchColor2b, pygame.Rect(0, 10, 10, 10))

    disappearingColor2a = 0, 255, 242
    disappearingTile2a.fill(borderColor)
    disappearingTile2a.fill(disappearingColor2a, pygame.Rect(1, 1, 18, 18))
    disappearingColor2d = 0, 96, 91
    disappearingTile2d.fill(borderColor)
    disappearingTile2d.fill(disappearingColor2d, pygame.Rect(1, 1, 18, 18))

    switchColor3a = 92, 119, 219
    switchColor3b = 153, 144, 237
    switchTile3.fill(switchColor3a, pygame.Rect(0, 0, 10, 10))
    switchTile3.fill(switchColor3b, pygame.Rect(10, 0, 10, 10))
    switchTile3.fill(switchColor3a, pygame.Rect(10, 10, 10, 10))
    switchTile3.fill(switchColor3b, pygame.Rect(0, 10, 10, 10))

    disappearingColor3a = 0, 55, 255
    disappearingTile3a.fill(borderColor)
    disappearingTile3a.fill(disappearingColor3a, pygame.Rect(1, 1, 18, 18))
    disappearingColor3d = 0, 24, 112
    disappearingTile3d.fill(borderColor)
    disappearingTile3d.fill(disappearingColor3d, pygame.Rect(1, 1, 18, 18))

    tpColor1a = 255, 137, 215
    tpColor1b = 237, 68, 180
    tpTile1.fill(tpColor1a, pygame.Rect(0, 0, 10, 10))
    tpTile1.fill(tpColor1b, pygame.Rect(10, 0, 10, 10))
    tpTile1.fill(tpColor1a, pygame.Rect(10, 10, 10, 10))
    tpTile1.fill(tpColor1b, pygame.Rect(0, 10, 10, 10))

    tpColor2a = 185, 56, 255
    tpColor2b = 124, 1, 191
    tpTile2.fill(tpColor2a, pygame.Rect(0, 0, 10, 10))
    tpTile2.fill(tpColor2b, pygame.Rect(10, 0, 10, 10))
    tpTile2.fill(tpColor2a, pygame.Rect(10, 10, 10, 10))
    tpTile2.fill(tpColor2b, pygame.Rect(0, 10, 10, 10))

    heroColor = 245, 249, 0
    hero.fill(heroColor, pygame.Rect(0, 0, 20, 20))

def minDigits(numStr, digits):
    """
    Helper function to return a string with a minimum number of digits
    :param numStr: string of the number to check
    :param digits: number of digits to have at a minimum
    :return: given string with the minimum number of digits
    """
    if len(numStr) < digits:
        for i in range(digits - len(numStr)):
            numStr = '0' + numStr
    return numStr

def keyPressed(key):
    """
    Checks to see if the given key is pressed
    :param key: key to check
    :return: whether or not the key is pressed
    """
    if keysJustPressed[key]:
        keysJustPressed[key] = False
        return True
    return False

def saveLevel(level):
    """
    Function to save levels in the correct format
    :param level: level number to save
    :return: None
    """
    saveFile = open("assets/levels/Level" + str(level) + ".txt", 'w')
    saveFile.truncate()
    for i in range(0, len(levelGrid)):
        for j in range(0, len(levelGrid[i])):
            saveFile.write(minDigits(str(levelGrid[i][j]), 2))
        saveFile.write('\n')
    saveFile.write(minDigits(str(spawn[0]), 2) + minDigits(str(spawn[1]), 2))
    saveFile.write('\n')

    saveFile.write(str(int(disappearingTilesOn[0])))
    saveFile.write('\n')

    saveFile.write(str(int(disappearingTilesOn[1])))
    saveFile.write('\n')

    saveFile.write(str(int(disappearingTilesOn[2])))
    saveFile.write('\n')

    saveFile.write(lvlTitle)

    saveFile.close()

def loadLevel(level):
    """
    Loads the level from the text file
    :param level: level number to load
    :return: None
    """
    global spawn, disappearingTilesOn
    global tp1Locations, tp2Locations, disappearingTilesInitState, lvlTitle

    tp1Locations = []
    tp2Locations = []

    try:
        saveFile = open("assets/levels/Level" + str(level) + ".txt")
        for i in range(0, 25):
            temp = saveFile.readline()
            for j in range (0, 25):
                temp2 = 2 * j
                temp3 = 2 * j + 2
                levelGrid[i][j] = int(temp[temp2:temp3])
                if levelGrid[i][j] == 10:
                    tp1Locations.append((i, j))
                elif levelGrid[i][j] == 11:
                    tp2Locations.append((i, j))

        temp = saveFile.readline()
        spawn = int(temp[0:2]), int(temp[2:4])

        disappearingTilesOn[0] = int(saveFile.readline())
        disappearingTilesOn[1] = int(saveFile.readline())
        disappearingTilesOn[2] = int(saveFile.readline())
        disappearingTilesInitState = list(disappearingTilesOn)

        lvlTitle = saveFile.readline()

        saveFile.close()
    except:
        wow = 2

def fillGameArea():
    """
    Fills the game area sprite with the tiles given the level information as well as the hero
    :return: None
    """
    for row in range(0, len(levelGrid)):
        for col in range(0, len(levelGrid[row])):
            if levelGrid[row][col] == 0:
                gameArea.blit(floorTile, pygame.Rect(col * 20, row * 20, 20, 20))
            elif levelGrid[row][col] == 1:
                gameArea.blit(wallTile, pygame.Rect(col * 20, row * 20, 20, 20))
            elif levelGrid[row][col] == 2:
                gameArea.blit(lavaTile, pygame.Rect(col * 20, row * 20, 20, 20))
            elif levelGrid[row][col] == 3:
                gameArea.blit(goalTile, pygame.Rect(col * 20, row * 20, 20, 20))
            elif levelGrid[row][col] == 4:
                gameArea.blit(switchTile1, pygame.Rect(col * 20, row * 20, 20, 20))
            elif levelGrid[row][col] == 5:
                if disappearingTilesOn[0]:
                    gameArea.blit(disappearingTile1a, pygame.Rect(col * 20, row * 20, 20, 20))
                else:
                    gameArea.blit(disappearingTile1d, pygame.Rect(col * 20, row * 20, 20, 20))
            elif levelGrid[row][col] == 6:
                gameArea.blit(switchTile2, pygame.Rect(col * 20, row * 20, 20, 20))
            elif levelGrid[row][col] == 7:
                if disappearingTilesOn[1]:
                    gameArea.blit(disappearingTile2a, pygame.Rect(col * 20, row * 20, 20, 20))
                else:
                    gameArea.blit(disappearingTile2d, pygame.Rect(col * 20, row * 20, 20, 20))
            elif levelGrid[row][col] == 8:
                gameArea.blit(switchTile3, pygame.Rect(col * 20, row * 20, 20, 20))
            elif levelGrid[row][col] == 9:
                if disappearingTilesOn[2]:
                    gameArea.blit(disappearingTile3a, pygame.Rect(col * 20, row * 20, 20, 20))
                else:
                    gameArea.blit(disappearingTile3d, pygame.Rect(col * 20, row * 20, 20, 20))
            elif levelGrid[row][col] == 10:
                gameArea.blit(tpTile1, pygame.Rect(col * 20, row * 20, 20, 20))
            elif levelGrid[row][col] == 11:
                gameArea.blit(tpTile2, pygame.Rect(col * 20, row * 20, 20, 20))
            elif levelGrid[row][col] == 12:
                if disappearingTilesOn[0]:
                    gameArea.blit(disappearingTile1d, pygame.Rect(col * 20, row * 20, 20, 20))
                else:
                    gameArea.blit(disappearingTile1a, pygame.Rect(col * 20, row * 20, 20, 20))
            elif levelGrid[row][col] == 13:
                if disappearingTilesOn[1]:
                    gameArea.blit(disappearingTile2d, pygame.Rect(col * 20, row * 20, 20, 20))
                else:
                    gameArea.blit(disappearingTile2a, pygame.Rect(col * 20, row * 20, 20, 20))
            elif levelGrid[row][col] == 14:
                if disappearingTilesOn[2]:
                    gameArea.blit(disappearingTile3d, pygame.Rect(col * 20, row * 20, 20, 20))
                else:
                    gameArea.blit(disappearingTile3a, pygame.Rect(col * 20, row * 20, 20, 20))
    if not heroPos[0] < 0:
        gameArea.blit(hero, pygame.Rect(heroPos[0], heroPos[1], 20, 20))

def renderFrame(msSinceStart):
    """
    Renders the entire frame with the game area and extra information and displays it
    :param msSinceStart: milliseconds since game start
    :return: None
    """
    screen.fill(backgroundClr)
    lvlLabel = largeFont.render("Level: " + str(currentLevel), True, (255, 255, 255))
    screen.blit(lvlLabel,
                pygame.Rect(10, (40 - lvlLabel.get_height()) / 2, lvlLabel.get_width(), lvlLabel.get_height()))
    timeLabel = largeFont.render(
        minDigits(str(int(msSinceStart / 1000.0 / 60.0)), 2) + ":" + minDigits(str(int(msSinceStart / 1000.0 % 60.0)),
                                                                               2), True, (255, 255, 255))
    screen.blit(timeLabel,
                pygame.Rect(450 - timeLabel.get_width() / 2, (40 - timeLabel.get_height()) / 2, timeLabel.get_width(),
                            timeLabel.get_height()))
    titleLabel = largeFont.render(lvlTitle, True, (255, 255, 255))
    screen.blit(titleLabel, pygame.Rect(250 - titleLabel.get_width() / 2, (40 - titleLabel.get_height()) / 2,
                                        titleLabel.get_width(), titleLabel.get_height()))
    fillGameArea()
    screen.blit(gameArea, pygame.Rect(0, 40, 500, 500))
    pygame.display.flip()

def main():
    """
    Plays the game starting from level 1
    :return: None
    """
    init()
    pygame.mixer.Sound("assets/audio/bckgrndMusic.wav").play(-1)

    global heroPos, disappearingTilesOn, heroVel, currentLevel
    dirMoving = None
    justStartedMoving = False
    while True:
        frameClock = pygame.time.Clock()
        msSinceStart = 0
        while currentLevel <= FINAL_LEVEL:
            loadLevel(currentLevel)
            heroPos = [spawn[0] * 20, spawn[1] * 20]
            won = False
            while not won:
                msSinceStart += frameClock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        keysDown[event.key] = True
                        keysJustPressed[event.key] = True
                    if event.type == pygame.KEYUP:
                        keysDown[event.key] = False
                        keysJustPressed[event.key] = False

                if keyPressed(114):
                    disappearingTilesOn = list(disappearingTilesInitState)
                    dirMoving = None
                    heroPos = [spawn[0] * 20, spawn[1] * 20]

                if dirMoving is None:
                    heroVel = [0, 0]
                    if keyPressed(97) or keyPressed(276):
                        dirMoving = "left"
                        justStartedMoving = True
                    if keyPressed(115) or keyPressed(274):
                        dirMoving = "down"
                        justStartedMoving = True
                    if keyPressed(100) or keyPressed(275):
                        dirMoving = "right"
                        justStartedMoving = True
                    if keyPressed(119) or keyPressed(273):
                        dirMoving = "up"
                        justStartedMoving = True
                if dirMoving == "left":
                    heroVel[0] = -speed
                elif dirMoving == "down":
                    heroVel[1] = speed
                elif dirMoving == "right":
                    heroVel[0] = speed
                elif dirMoving == "up":
                    heroVel[1] = -speed

                if not justStartedMoving and float(heroPos[0] / 20.0).is_integer() and float(heroPos[1] / 20.0).is_integer():
                    if levelGrid[int(heroPos[1] / 20)][int(heroPos[0] / 20)] == 2:
                        disappearingTilesOn = list(disappearingTilesInitState)
                        dirMoving = None
                        heroPos = [spawn[0] * 20, spawn[1] * 20]
                    elif levelGrid[int(heroPos[1] / 20)][int(heroPos[0] / 20)] == 4:
                        if dirMoving is not None:
                            disappearingTilesOn[0] = not disappearingTilesOn[0]
                    elif levelGrid[int(heroPos[1] / 20)][int(heroPos[0] / 20)] == 6:
                        if dirMoving is not None:
                            disappearingTilesOn[1] = not disappearingTilesOn[1]
                    elif levelGrid[int(heroPos[1] / 20)][int(heroPos[0] / 20)] == 8:
                        if dirMoving is not None:
                            disappearingTilesOn[2] = not disappearingTilesOn[2]
                    elif levelGrid[int(heroPos[1] / 20)][int(heroPos[0] / 20)] == 10:
                        if dirMoving is not None:
                            if (int(heroPos[1] / 20), int(heroPos[0] / 20)) == tp1Locations[0]:
                                heroPos = [tp1Locations[1][1] * 20, tp1Locations[1][0] * 20]
                            else:
                                heroPos = [tp1Locations[0][1] * 20, tp1Locations[0][0] * 20]
                    elif levelGrid[int(heroPos[1] / 20)][int(heroPos[0] / 20)] == 11:
                        if dirMoving is not None:
                            if (int(heroPos[1] / 20), int(heroPos[0] / 20)) == tp2Locations[0]:
                                heroPos = [tp2Locations[1][1] * 20, tp2Locations[1][0] * 20]
                            else:
                                heroPos = [tp2Locations[0][1] * 20, tp2Locations[0][0] * 20]
                elif justStartedMoving:
                    justStartedMoving = False

                if dirMoving == "right":
                    xIndex = int(math.floor((heroPos[0] + heroVel[0] + 15) / 20))
                else:
                    xIndex = int(math.floor((heroPos[0] + heroVel[0]) / 20))
                if dirMoving == "down":
                    yIndex = int(math.floor((heroPos[1] + heroVel[1] + 15) / 20))
                else:
                    yIndex = int(math.floor((heroPos[1] + heroVel[1]) / 20))

                if dirMoving is not None:
                    if xIndex in range(25) and yIndex in range(25):
                        if levelGrid[yIndex][xIndex] == 1 or \
                            disappearingTilesOn[0] and levelGrid[yIndex][xIndex] == 5 or \
                            disappearingTilesOn[1] and levelGrid[yIndex][xIndex] == 7 or \
                            disappearingTilesOn[2] and levelGrid[yIndex][xIndex] == 9 or \
                            not disappearingTilesOn[0] and levelGrid[yIndex][xIndex] == 12 or \
                            not disappearingTilesOn[1] and levelGrid[yIndex][xIndex] == 13 or \
                            not disappearingTilesOn[2] and levelGrid[yIndex][xIndex] == 14:
                            dirMoving = None
                        else:
                            heroPos[0] += heroVel[0]
                            heroPos[1] += heroVel[1]
                    else:
                        dirMoving = None
                elif levelGrid[yIndex][xIndex] == 3:
                    won = True

                renderFrame(msSinceStart)
                #while not won
            currentLevel += 1
            #while currentLevel <= finalLevel
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    keysDown[event.key] = True
                    keysJustPressed[event.key] = True
                if event.type == pygame.KEYUP:
                    keysDown[event.key] = False
                    keysJustPressed[event.key] = False

            if keyPressed(114):
                currentLevel = 1
                break

            screen.fill(backgroundClr)
            timeLabel = largeFont.render(minDigits(str(int(msSinceStart / 1000.0 / 60.0)), 2) + ":" + minDigits(
                str(int(msSinceStart / 1000.0 % 60.0)), 2), True, (255, 255, 255))
            screen.blit(timeLabel, pygame.Rect(250 - timeLabel.get_width() / 2, (270 - timeLabel.get_height()) / 2,
                                               timeLabel.get_width(), timeLabel.get_height()))
            pygame.display.flip()

if __name__ == "__main__":
    main()