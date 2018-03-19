I chose to integrate both games in one program, games.py. This makes it essentially a suite of games.
I wanted it to be as easy as possible to add a game. I did this by making games.py with as little hardcoding as possible.
The dictionary/key method enables the code both to easily check whether a game the user asked for exists and to quickly call the correct
game. It also automatically iterates through all the available games.
To add a game, the only thing you need to do is import it and add it to the dictionary.

For hangman, I chose not to use a picture. I did this so it is really easy to change the number of chances you get.
All you need to do is change the variable MAX_MISTAKES. I considered many images that could be sliced together,
but I decided that was too complicated for this project.
Although there are two ways to win (all letters or word as a whole),
I chose not to factor out the winning screen into its own function. It was small enough that I chose to sacrifice a
small amount of redundancy for better readability.

Dictionary was taken from the speller pset.

For minesweeper, I decided ncurses would take too long. I made colors because they're pretty.
I didn't use background for each letter because they would blend into each other and make the board not pretty.
I used these colors specifically because they had good cotrast with each other making the board both more readable and more pretty.
I took away the board when help messages pop up to make it easier to see the important message.
I cleared the screen each time to avoid multiple things cluttering the screen.

I factored out play_again because it could be used in multiple places and in both programs.