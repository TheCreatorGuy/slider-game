import SliderGame

if __name__ == "__main__":
    SliderGame.currentLevel = raw_input("What level do you want to test?\n")
    SliderGame.finalLevel = SliderGame.currentLevel
    SliderGame.main()