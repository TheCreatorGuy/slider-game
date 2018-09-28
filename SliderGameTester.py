import SliderGame

if __name__ == "__main__":
    SliderGame.currentLevel = raw_input("What level do you want to test?\n")
    SliderGame.FINAL_LEVEL = SliderGame.currentLevel
    SliderGame.main()