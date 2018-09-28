"""
Filename: slidergame_solver.py
Interpreter: 2.7
Author: Tim Johnson
Description: A project designed to find the best solution to every level of my slider game.
"""
import SliderGame as sg
import copy

DOWN = "V"
LEFT = "<"
RIGHT = ">"
UP = "^"
DIRECTIONS = [DOWN, LEFT, RIGHT, UP]

X_IDX = 0
Y_IDX = 1

class LevelState:
    toggletile_states = None
    tp1_locs = None
    tp2_locs = None
    hero_x = -1
    hero_y = -1

    path = ""
    failed = False
    complete = False

    def __init__(self, toggletile_states, tp1_locs, tp2_loc, hero_x, hero_y):
        self.toggletile_states = toggletile_states
        self.tp1_locs = tp1_locs
        self.tp2_locs = tp2_loc
        self.hero_x = hero_x[X_IDX]
        self.hero_y = hero_y[Y_IDX]

    def __copy__(self):
        return LevelState(self.toggletile_states, self.tp1_locs, self.tp2_locs, self.hero_x, self.hero_y)

    def next_step(self, direction):
        self.path += direction

        vert = 0
        hor = 0
        if direction == DOWN:
            vert = 1
        elif direction == UP:
            vert = -1
        elif direction == RIGHT:
            hor = 1
        elif direction == LEFT:
            hor = -1
        while 0 <= self.hero_y < sg.GRID_SIZE :
            if not 0 <= self.hero_x+hor < sg.GRID_SIZE and not 0 <= self.hero_y+vert < sg.GRID_SIZE:
                break

            pos = sg.levelGrid[self.hero_y+vert][self.hero_x+hor]
            if  pos == sg.ID_WALL or \
                    self.toggletile_states[0]       and pos == sg.ID_ORANGE_TILE_OFF    or \
                    self.toggletile_states[1]       and pos == sg.ID_TEAL_TILE_OFF      or \
                    self.toggletile_states[2]       and pos == sg.ID_BLUE_TILE_OFF      or \
                    not self.toggletile_states[0]   and pos == sg.ID_ORANGE_TILE_ON     or \
                    not self.toggletile_states[1]   and pos == sg.ID_TEAL_TILE_ON       or \
                    not self.toggletile_states[2]   and pos == sg.ID_BLUE_TILE_ON:
                break

            self.hero_x += hor
            self.hero_y += vert

            if pos == sg.ID_ORANGE_BUTTON:
                self.toggletile_states[0] = not self.toggletile_states[0]
            elif pos == sg.ID_TEAL_BUTTON:
                self.toggletile_states[1] = not self.toggletile_states[1]
            elif pos == sg.ID_BLUE_BUTTON:
                self.toggletile_states[2] = not self.toggletile_states[2]
            elif pos == sg.ID_LAVA:
                self.failed = True
            elif pos == sg.ID_GOAL:
                self.complete = True
            elif pos == sg.ID_PINK_TP:
                if self.tp1_locs[0] == (self.hero_y, self.hero_x):
                    (self.hero_y, self.hero_x) = self.tp1_locs[1]
                else:
                    (self.hero_y, self.hero_x) = self.tp1_locs[0]
            elif pos == sg.ID_PURPLE_TP:
                if self.tp2_locs[0] == (self.hero_y, self.hero_x):
                    (self.hero_y, self.hero_x) = self.tp2_locs[1]
                else:
                    (self.hero_y, self.hero_x) = self.tp2_locs[0]

    def next_gen(self):
        next_list = []
        for direction in DIRECTIONS:
            if self.path[-1:] != direction:
                new_state = copy.copy(self)
                new_state.next_step(direction)
                next_list.append(new_state)
        return next_list


def level_to_class(level_num):
    sg.loadLevel(level_num)
    return LevelState(sg.disappearingTilesOn, sg.tp1Locations, sg.tp2Locations, sg.heroPos[X_IDX], sg.heroPos[Y_IDX])

def find_solution(level_state):
    return ""

def main():
    """
    Finds the solution to every level of the slider game and stores in a solution file.
    :return: None
    """
    for level in range(1, sg.FINAL_LEVEL+1):
        level_state = level_to_class(level)
        path = find_solution(level_state)
        savefile = open("assets/solutions/Level" + str(level) + "solution.sol", 'w')
        savefile.write(path);

if __name__ == "__main__":
    main()