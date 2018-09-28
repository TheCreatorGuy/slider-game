import pygame, sys, math, SliderGame

mousePos = [0,0]

def setTile(tile):
    row = int(math.floor(mousePos[1] / 20))
    column = int(math.floor(mousePos[0] / 20))
    SliderGame.levelGrid[row][column] = tile

def main():
    SliderGame.init()
    SliderGame.screen = pygame.display.set_mode((500, 500))

    level = raw_input("What level do you want to edit?\n")
    SliderGame.loadLevel(level)

    global mousePos
    while True:
        mousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                SliderGame.saveLevel(level)
                sys.exit()
            if event.type == pygame.KEYDOWN:
                SliderGame.keysDown[event.key] = True
                SliderGame.keysJustPressed[event.key] = True
            if event.type == pygame.KEYUP:
                SliderGame.keysDown[event.key] = False
                SliderGame.keysJustPressed[event.key] = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                row = int(math.floor(mousePos[1] / 20))
                column = int(math.floor(mousePos[0] / 20))
                if SliderGame.levelGrid[row][column] == 4 or SliderGame.levelGrid[row][column] == 5 or \
                                SliderGame.levelGrid[row][column] == 12:
                    SliderGame.disappearingTilesOn[0] = not SliderGame.disappearingTilesOn[0]
                if SliderGame.levelGrid[row][column] == 6 or SliderGame.levelGrid[row][column] == 7 or \
                                SliderGame.levelGrid[row][column] == 13:
                    SliderGame.disappearingTilesOn[1] = not SliderGame.disappearingTilesOn[1]
                if SliderGame.levelGrid[row][column] == 8 or SliderGame.levelGrid[row][column] == 9 or \
                                SliderGame.levelGrid[row][column] == 14:
                    SliderGame.disappearingTilesOn[2] = not SliderGame.disappearingTilesOn[2]

        if SliderGame.keysDown[49]:
            setTile(0)
        if SliderGame.keysDown[113]:
            setTile(1)
        if SliderGame.keysDown[97]:
            setTile(2)
        if SliderGame.keysDown[121]:
            setTile(3)
        if SliderGame.keysDown[54]:
            row = int(math.floor(mousePos[1] / 20))
            column = int(math.floor(mousePos[0] / 20))
            SliderGame.spawn = column, row
        if SliderGame.keysDown[51]:
            setTile(4)
        if SliderGame.keysDown[101]:
            setTile(5)
        if SliderGame.keysDown[52]:
            setTile(6)
        if SliderGame.keysDown[114]:
            setTile(7)
        if SliderGame.keysDown[53]:
            setTile(8)
        if SliderGame.keysDown[116]:
            setTile(9)
        if SliderGame.keysDown[50]:
            setTile(10)
        if SliderGame.keysDown[119]:
            setTile(11)
        if SliderGame.keysDown[100]:
            setTile(12)
        if SliderGame.keysDown[102]:
            setTile(13)
        if SliderGame.keysDown[103]:
            setTile(14)
        if SliderGame.keyPressed(32):
            temp = raw_input("What should the title be? Enter nothing to use the previous title: " + SliderGame.lvlTitle + '\n')
            if temp is not "":
                SliderGame.lvlTitle = temp
        if SliderGame.keyPressed(13):
            SliderGame.saveLevel(level)
            sys.exit()

        SliderGame.screen.fill(SliderGame.backgroundClr)
        SliderGame.fillGameArea()
        SliderGame.gameArea.blit(SliderGame.hero, pygame.Rect(SliderGame.spawn[0] * 20, SliderGame.spawn[1] * 20, 20, 20))
        SliderGame.screen.blit(SliderGame.gameArea, pygame.Rect(0, 0, 500, 500))
        pygame.display.flip()

if __name__ == "__main__":
    main()