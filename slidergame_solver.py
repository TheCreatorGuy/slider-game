"""
Filename: slidergame_solver.py
Interpreter: 2.7
Author: Tim Johnson
Description: A project designed to find the best solution to every level of my slider game.
"""
import SliderGame as sg
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
    failed = False
    complete = False
    depth = 0
    prev_node = None
    next_nodes = None

    def __init__(self, toggletile_states, tp1_locs, tp2_loc, hero_x, hero_y):
        """
        Creates the new LevelState
        :param toggletile_states: states of the toggle tiles in list form [ORANGE, TEAL, BLUE]
        :param tp1_locs: locations of the pink teleporters as a list of tuples [(y, x), (y, x)]
        :param tp2_loc: locations of the purple teleporters as a list of tuples
        :param hero_x: x coordinate of the hero
        :param hero_y: y coordinate of the hero
        """
        self.toggletile_states = toggletile_states
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
        cpy.prev_node = self
        cpy.path = self.path
        cpy.depth = self.depth
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
        :return: None
        """
        self.path += direction #This is how we get the path in the end

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
        while 0 <= self.hero_y < sg.GRID_SIZE :
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
                self.failed = True

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

    def next_gen(self):
        """
        Generate the next_nodes given every direction except the last hit direction (because that should
        theoretically never move us) and any direction that would give us a state that is equivalent
        to one that we have already reached in this or another branch, but in fewer moves
        :return: None
        """
        # Failsafe so we don't do this twice
        if self.next_nodes is not None:
            return
        self.next_nodes = []

        # Make a new state for every direction
        for direction in DIRECTIONS:
            if self.path[-1:] != direction: #except the last direction
                new_state = copy.copy(self)
                new_state.depth += 1 #keep track of depth so we can disregard superfluous states
                new_state.next_step(direction) #change state so we can verify if it is a repeat

                # Check every previous state on this branch to see if they are the same. If so,
                # it is a repeated state and should not be used again.
                repeat_state = False
                back_step = self
                while back_step is not None:
                    if new_state.equals(back_step):
                        repeat_state = True
                        break
                    back_step = back_step.prev_node
                if not repeat_state:
                    self.next_nodes.append(new_state)


def level_to_class(level_num):
    """
    Takes the information from SliderGame.py and converts it into the initial LevelState class to find
    the solution of
    :param level_num: the level number to get the class of
    :return: the corresponding LevelState
    """
    sg.loadLevel(level_num)
    return LevelState(sg.disappearingTilesInitState, sg.tp1Locations, sg.tp2Locations,
                      sg.spawn[0], sg.spawn[1])

def find_solution(tree_start):
    """
    The wrapper function to find the best path to solve the level from the start node given
    :param tree_start: starting LevelState node for the level to be solved
    :return: string for the smallest possible sequence of inputs to solve the level, or "unsolvable"
                if the solver ran through every possible solution but none was successful
    """
    best_solution = find_solution_rec(tree_start)
    if best_solution is None:
        return "unsolvable"
    return best_solution.path

def find_solution_rec(current_node, best_depth=sys.maxint):
    """
    Recursively finds any completed nodes from the children of the current node
    :param current_node: the node to check for children
    :param best_depth: limiter depth so we abort any trees that would be suboptimal
    :return: node with the best solution of all children, or None if there was no better solution
                than the given best_depth
    """
    if current_node.depth+1 >= best_depth:
        return None

    current_node.next_gen()
    for node in current_node.next_nodes:
        if node.complete:
            return node

    best_successor = None
    for node in current_node.next_nodes:
        if not node.failed:
            potential_successor = find_solution_rec(node, best_depth)
            if potential_successor is not None:
                best_depth = potential_successor.depth
                best_successor = potential_successor

    return best_successor

def main():
    """
    Finds the solution to every level of the slider game and stores in a solution file.
    :return: None
    """
    print "Finding solutions to the SliderGame levels! Hold on tight!\n"
    #max_test = sg.FINAL_LEVEL
    max_test = 4
    for level in range(1, max_test+1):
        print "Finding Solution for level " + str(level) + "..."
        level_state = level_to_class(level)
        path = find_solution(level_state)
        print "Solution found! The answer is: " + path + '\n'
        savefile = open("assets/solutions/Level" + str(level) + "solution.sol", 'w')
        savefile.write(path)

if __name__ == "__main__":
    main()