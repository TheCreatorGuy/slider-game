"""
Filename: slider_editor.py
Interpreter: 2.7
Author: Tim Johnson
Description: A helper script to edit the levels graphically using keystrokes and the mouse position
"""
import pygame, sys, math, slidergame

# Probably doesn't need to be global
mousePos = [0,0]

def setTile(tile):
    """
    Sets the tile under the mouse to the type given
    :param tile: id of the tile type to set
    :return: None
    """
    row = int(math.floor(mousePos[1] / 20))
    column = int(math.floor(mousePos[0] / 20))
    slidergame.levelGrid[row][column] = tile

def main():
    """
    Edits the level specified
    :return:
    """
    slidergame.init()
    slidergame.screen = pygame.display.set_mode((500, 500))
    
    if len(sys.argv) != 2:
        level = raw_input("What level do you want to edit?\n")
    else:
        level = int(sys.argv[1])
    slidergame.loadLevel(level)

    global mousePos
    while True:
        mousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                slidergame.saveLevel(level)
                sys.exit()
            if event.type == pygame.KEYDOWN:
                slidergame.keysDown[event.key] = True
                slidergame.keysJustPressed[event.key] = True
            if event.type == pygame.KEYUP:
                slidergame.keysDown[event.key] = False
                slidergame.keysJustPressed[event.key] = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                row = int(math.floor(mousePos[1] / 20))
                column = int(math.floor(mousePos[0] / 20))
                if slidergame.levelGrid[row][column] == 4 or slidergame.levelGrid[row][column] == 5 or \
                                slidergame.levelGrid[row][column] == 12:
                    slidergame.disappearingTilesOn[0] = not slidergame.disappearingTilesOn[0]
                if slidergame.levelGrid[row][column] == 6 or slidergame.levelGrid[row][column] == 7 or \
                                slidergame.levelGrid[row][column] == 13:
                    slidergame.disappearingTilesOn[1] = not slidergame.disappearingTilesOn[1]
                if slidergame.levelGrid[row][column] == 8 or slidergame.levelGrid[row][column] == 9 or \
                                slidergame.levelGrid[row][column] == 14:
                    slidergame.disappearingTilesOn[2] = not slidergame.disappearingTilesOn[2]

        if slidergame.keysDown[49]:
            setTile(0)
        if slidergame.keysDown[113]:
            setTile(1)
        if slidergame.keysDown[97]:
            setTile(2)
        if slidergame.keysDown[121]:
            setTile(3)
        if slidergame.keysDown[54]:
            row = int(math.floor(mousePos[1] / 20))
            column = int(math.floor(mousePos[0] / 20))
            slidergame.spawn = column, row
        if slidergame.keysDown[51]:
            setTile(4)
        if slidergame.keysDown[101]:
            setTile(5)
        if slidergame.keysDown[52]:
            setTile(6)
        if slidergame.keysDown[114]:
            setTile(7)
        if slidergame.keysDown[53]:
            setTile(8)
        if slidergame.keysDown[116]:
            setTile(9)
        if slidergame.keysDown[50]:
            setTile(10)
        if slidergame.keysDown[119]:
            setTile(11)
        if slidergame.keysDown[100]:
            setTile(12)
        if slidergame.keysDown[102]:
            setTile(13)
        if slidergame.keysDown[103]:
            setTile(14)
        if slidergame.keyPressed(32):
            temp = raw_input("What should the title be? Enter nothing to use the previous title: " + slidergame.lvlTitle + '\n')
            if temp is not "":
                slidergame.lvlTitle = temp
        if slidergame.keyPressed(13):
            slidergame.saveLevel(level)
            sys.exit()

        slidergame.screen.fill(slidergame.backgroundClr)
        slidergame.fillGameArea()
        slidergame.gameArea.blit(slidergame.hero, pygame.Rect(slidergame.spawn[0] * 20, slidergame.spawn[1] * 20, 20, 20))
        slidergame.screen.blit(slidergame.gameArea, pygame.Rect(0, 0, 500, 500))
        pygame.display.flip()

if __name__ == "__main__":
    main()