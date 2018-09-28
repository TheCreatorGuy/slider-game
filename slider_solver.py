"""
Filename: slider_solver.py
Interpreter: 2.7
Author: Tim Johnson
Description: A project designed to find the best solution to every level of my slider game.
"""
import slidergame as sg
import Queue as q
import copy
import sys

# Constants for direction enumeration
DOWN = "V"
LEFT = "<"
RIGHT = ">"
UP = "^"
DIRECTIONS = [DOWN, LEFT, RIGHT, UP]

class LevelState:
    """
    A class to represent a node of the solution for a given level. To find the solution, the current level state
    generates its own children and checks for validity given all previous states generated
    """
    # Level information
    toggletile_states = None
    tp1_locs = None
    tp2_locs = None
    hero_x = -1
    hero_y = -1

    # Node information
    path = ""
    complete = False

    def __init__(self, toggletile_states, tp1_locs, tp2_loc, hero_x, hero_y):
        """
        Creates the new LevelState
        :param toggletile_states: states of the toggle tiles in list form [ORANGE, TEAL, BLUE]
        :param tp1_locs: locations of the pink teleporters as a list of tuples [(y, x), (y, x)]
        :param tp2_loc: locations of the purple teleporters as a list of tuples
        :param hero_x: x coordinate of the hero
        :param hero_y: y coordinate of the hero
        """
        self.toggletile_states = list(toggletile_states)
        self.tp1_locs = tp1_locs
        self.tp2_locs = tp2_loc
        self.hero_x = hero_x
        self.hero_y = hero_y

    def __copy__(self):
        """
        Copies all values except "failed", "complete", "prev_node", and "next_nodes". Sets
        "prev_node" to the original being copied from
        :return: new copy of the node
        """
        cpy = LevelState(self.toggletile_states, self.tp1_locs, self.tp2_locs, self.hero_x, self.hero_y)
        cpy.path = self.path
        return cpy

    def equals(self, other):
        """
        Finds whether or not the given node is equivalent to this node with all information that matters
        :param other: the node being compared to this node
        :return: True if the nodes are equivalent, False otherwise
        """
        return self.toggletile_states == other.toggletile_states and self.hero_x == other.hero_x and self.hero_y == other.hero_y

    def next_step(self, direction):
        """
        Sets the state information of this state to what it would be if the player had input the
        direction supplied to this function
        :param direction: direction to move the hero
        :return: whether or not this step succeeded
        """
        self.path += direction  # This is how we get the path in the end

        # For the sake of reusing code, the position is verified relatively
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
        while 0 <= self.hero_y < sg.GRID_SIZE:
            # If the next movement would be out of bounds, do not move the player and end movement
            if self.hero_x+hor < 0 or self.hero_x+hor >= sg.GRID_SIZE or \
                    self.hero_y+vert < 0 or self.hero_y+vert >= sg.GRID_SIZE:
                break

            pos = sg.levelGrid[self.hero_y+vert][self.hero_x+hor]

            # If the next position is a solid block, do not move the player and end movement
            if  pos == sg.ID_WALL or \
                    self.toggletile_states[0]       and pos == sg.ID_ORANGE_TILE_OFF    or \
                    self.toggletile_states[1]       and pos == sg.ID_TEAL_TILE_OFF      or \
                    self.toggletile_states[2]       and pos == sg.ID_BLUE_TILE_OFF      or \
                    not self.toggletile_states[0]   and pos == sg.ID_ORANGE_TILE_ON     or \
                    not self.toggletile_states[1]   and pos == sg.ID_TEAL_TILE_ON       or \
                    not self.toggletile_states[2]   and pos == sg.ID_BLUE_TILE_ON:
                break

            # The next space is free, so move there
            self.hero_x += hor
            self.hero_y += vert

            # If the position was lava, this state is a failed state
            if pos == sg.ID_LAVA:
                return False

            # Toggle any buttons
            if pos == sg.ID_ORANGE_BUTTON:
                self.toggletile_states[0] = not self.toggletile_states[0]
            elif pos == sg.ID_TEAL_BUTTON:
                self.toggletile_states[1] = not self.toggletile_states[1]
            elif pos == sg.ID_BLUE_BUTTON:
                self.toggletile_states[2] = not self.toggletile_states[2]

            # Move the hero to the other teleporter location if we are now on one
            if pos == sg.ID_PINK_TP:
                if self.tp1_locs[0] == (self.hero_y, self.hero_x):
                    (self.hero_y, self.hero_x) = self.tp1_locs[1]
                else:
                    (self.hero_y, self.hero_x) = self.tp1_locs[0]
            elif pos == sg.ID_PURPLE_TP:
                if self.tp2_locs[0] == (self.hero_y, self.hero_x):
                    (self.hero_y, self.hero_x) = self.tp2_locs[1]
                else:
                    (self.hero_y, self.hero_x) = self.tp2_locs[0]

        # Now that we are done moving, check to see if we are on the goal
        if sg.levelGrid[self.hero_y][self.hero_x] == sg.ID_GOAL:
            self.complete = True

        return True

    def next_gen(self, prev_loc_grid):
        """
        Generate the next_nodes given every direction except the last hit direction (because that should
        theoretically never move us) and any direction that would give us a state that is equivalent
        to one that we have already reached in this or another branch, but in fewer moves
        :param: prev_loc_grid: a grid of lists. This grid should be the same dimensions of the level. It is
                    modified here so that if a new state does not find itself repeating on this grid, it
                    adds itself. If it is on the grid, it does not add itself to the next_nodes
        :return: list of the next generation of states, or children
        """
        # Failsafe so we don't do this twice
        children = []

        # Make a new state for every direction
        for direction in DIRECTIONS:
            if self.path[-1:] != direction:  # except the last direction
                new_state = copy.copy(self)
                if not new_state.next_step(direction):  # change state so we can verify if it is a repeat
                    continue

                # Check new state to see if it repeats in the prev_loc_grid. If it isn't, use it
                if not new_state.toggletile_states in prev_loc_grid[new_state.hero_y][new_state.hero_x]:
                    prev_loc_grid[new_state.hero_y][new_state.hero_x].append(new_state.toggletile_states)
                    children.append(new_state)

        return children


def level_to_class(level_num):
    """
    Takes the information from slidergame.py and converts it into the initial LevelState class to find
    the solution of
    :param level_num: the level number to get the class of
    :return: tuple of the corresponding LevelState and the previous location grid with the start state included
    """
    sg.loadLevel(level_num)
    prev_loc_grid = [[[] for _ in range(sg.GRID_SIZE)] for _ in range(sg.GRID_SIZE)]
    start_node = LevelState(sg.disappearingTilesInitState, sg.tp1Locations, sg.tp2Locations, sg.spawn[0], sg.spawn[1])
    prev_loc_grid[start_node.hero_y][start_node.hero_x].append(start_node.toggletile_states)
    return start_node, prev_loc_grid


def find_solution(level_num):
    """
    Finds the solution to the given level and returns its path, unless it is unsolvable
    :param level_num: level to find the solution of
    :return: the path of the solution, or "unsolvable" if there is no solution
    """
    ret = "unsolvable"

    # Setup
    start_node, prev_loc_grid = level_to_class(level_num)
    nodequeue = q.Queue()
    nodequeue.put(start_node)

    # Repeat getting the first node from the queue while there is one. If there isn't one, then
    # there was no successful state, making it unsolvable.
    while not nodequeue.empty():
        current_node = nodequeue.get()
        sys.stdout.write("\rCurrently testing: " + current_node.path)  # Overwrite testing line for "loading" look
        sys.stdout.flush()

        # If it was complete, we have found the optimal solution, because of the nature of the queue. If a path is
        # tested, it means that all shorter paths failed.
        if current_node.complete:
            ret = current_node.path
            break

        # For each child, add it to the queue so that we can test it later
        children = current_node.next_gen(prev_loc_grid)
        for child in children:
            nodequeue.put(child)

    sys.stdout.write("\r")
    return ret


def main():
    """
    Finds the solution to every level of the slider game and stores in a solution file.
    :return: None
    """
    print "Finding solutions to the SliderGame levels! Hold on tight!\n"
    for level in range(1, sg.FINAL_LEVEL+1):
        print "Finding Solution for level " + str(level) + "..."
        path = find_solution(level)
        print "Solution found! The answer is: (" + path + "), comprising of " + str(len(path)) + " moves\n"
        savefile = open("assets/solutions/Level" + str(level) + "solution.sol", 'w')
        savefile.write(path)
        savefile.close()


if __name__ == "__main__":
    main()
