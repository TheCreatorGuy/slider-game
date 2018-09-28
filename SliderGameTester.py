import SliderGame, sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        SliderGame.currentLevel = int(raw_input("What level do you want to test? "))
    else:
        SliderGame.currentLevel = int(sys.argv[1])
    SliderGame.FINAL_LEVEL = SliderGame.currentLevel
    SliderGame.main()