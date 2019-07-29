# Plays a suite of games, as determined by the dictionary "game_options" and the imported programs


import sys

import hangman
import minesweeper

game_options = {"hangman": hangman.hangman, "minesweeper": minesweeper.minesweeper}


def main():
    # check usage
    if len(sys.argv) < 2:
        print("usage: games.py game [game options]")
        return 1

    # play selected game if available or tell user if not
    if sys.argv[1] in game_options:
        game_options[sys.argv[1]](sys.argv[1:])
    else:
        print("Games available: " + ", ".join(game_options))

if __name__ == "__main__":
    main()