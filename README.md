This project allows you to play either hangman or minesweeper in your terminal window.
Only tested in linux. Screen clear method may not work in windows. But that's what you get for using windows.

To play a game, navigate in a fresh terminal window to the finalproject folder. Type in `python games.py` notice the error message.
You need to choose which game to play! You can do this by typing either `hangman` or `minesweeper` after games.py.
Basic gameplay is thus `python games.py hangman` or `python games.py minesweeper`.
You may also play the game directly via `python hangman.py` or `python minesweeper.py`.


Minesweeper:
For game rules, see here: https://en.wikipedia.org/wiki/Minesweeper_(video_game)
In the game, the numbers at the very left and very top are row and column numbers. Question marks indicate unrevealed squares.
'f' means a flag has been placed. When you lose, 'b' means a bomb was there.
Pretty color-coding will make this easier.

Once game has started, type in row and column number to reveal question mark. Format is row (space) column.
For example, if you want to reveal row 4, column 5, type `4 5`.
To place a flag instead of revealing, type in 'f' after the row number. You do the same to remove a flag
For example: `4 5 f`
You cannot reveal a square where a flag has been placed.
You win when a flag has been placed on every bomb, and no flags have been placed on non-bombs.



Extra options:
In command line when starting the game, you have the option of changing the size of the game and the number of bombs.
You do this with two command line arguments. The first must be the size of the screen you want and the second must be the number of bombs
For example, if you want 25 bombs on a 30x30 screen, type `python games.py hangman 30 25`.


Hangman:
For game rules see here: https://en.wikipedia.org/wiki/Hangman_(game)
Once game has started, type in '1' for 1-player or '2' for 2 player version

1 player:
Computer selects random word from dictionary. Guess letters until you have used up all your chances or the entire word is revealed.
If you want, you may type in the entire word you are guessing. If you're right, you win. Wrong, it counts as a mistake.
The dashes represnt the unrevealed letter of the word. The list of letters above the word is the letters you have already guessed.
If you guess a letter or word you have already guessed, it does not count as a mistake.

2 player:
Prompts user for word. Word must be in dictionary. Screen will clear once you enter word.
Gameplay proceeds from there the same as in 1 player mode.


Extra options:
The default dictionary countains many words. You may change the dictionary by typing in an extra command line argument with the path
to the dictionary.
Example:
`python games.py hangman ~/workspace/finalproject/dictionary2`

