"""
Filename: slider_solver.py
Interpreter: 2.7
Author: Tim Johnson
Description: A project designed to find the best solution to every level of my slider game.
"""
import slidergame, sys

def main():
    if len(sys.argv) != 2:
        slidergame.currentLevel = int(raw_input("What level do you want to test? "))
    else:
        slidergame.currentLevel = int(sys.argv[1])
    slidergame.FINAL_LEVEL = slidergame.currentLevel
    slidergame.main()


if __name__ == "__main__":
    main()