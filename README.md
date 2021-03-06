# Slider Game

This "Slider Game" was a project initially started for my Senior Project in high school, which was an open ended research/application project that I did about video game creation. Later, I decided to port the project to JavaScript as an exercise in learning the language and refactoring.

## JavaScript Version

I am currently hosting this version on my [website](http://itstimjohnson.com/slider.html), however you can also run it directly from the given slider.html file. Unfortunately, Google Chrome doesn't understand that a file originating on your local machine might have a legitimate reason to access local files, so you will have to use another browser if you choose to do it this way, I used FireFox. The issue with this version is that it uses far more memory than it needs to because it redraws the background every frame, making it run slower than the python version.

## Python Version

The Python version was built with Python2.7 and pygame.

### Setup

1.  To start, if you don't have it already, install Python2.7 [here](https://www.python.org/downloads/release/python-2713/). Make sure to check the "add to path" option.

2.  After installation, I would recommend renaming the "python.exe" file that was just created to "python27.exe" to avoid confusion with other versions. I don't recommend using version 2.7 for anything more than running old programs like this.

3.  Open the command line and run the following command:

```
python27 -m pip install pygame
```

4.  Now we are ready to run the game. Either clone it or download the .zip and extract it.

5.  In the command line, navigate to the location of the repository using 

```
cd path-to-folder
```

6.  Finally, execute the game with 

```
python27 slidergame.py
```

Enjoy!

# Slider Solver

With the game comes packaged a more recent project aimed at solving every puzzle using the smallest number of moves. To run this, follow the steps for running the game except type `python27 slider_solver.py` instead of `python27 slidergame.py`

# Other Files

The other files packaged within are helper scripts that I used to create the levels. At the moment, it is very hard to read and use them without prior knowledge of the game, so I would not recommend creating your own levels with them yet. If you want to dive into the code to see how they work and try to piece together how to use them, go for it, but you were warned.
