# Plays minesweeper in terminal window

# libraries to import
from cs50 import get_string
from cs50 import get_float
from cs50 import get_char
from termcolor import colored
import os
import sys
import time
import random
import string

import helpers

# constants
DEFAULT_SIZE = 10  # tested for maximal funness
DEFAULT_BOMBS = 11  # tested for maximal funness
SIZE_MAX = 60  # otherwise, won't fit in terminal window


class square:
    def __init__(self):
        self.revealed = False
        self.nearby = 0
        self.bomb = False
        self.flag = False


def minesweeper(sysArgs):
    # suppress traceback
    sys.tracebacklimit = 0

    # clear screen
    unused_variable = os.system('clear')
    print("\12")

    # determine size and number of flags
    # user inputted
    if len(sysArgs) == 3:
        try:
            # check validity of size
            size = int(sysArgs[1])
            if not 0 < size <= SIZE_MAX:
                print(colored("size of screen must be from 1 to 60", "red"))
                return
            # check validity of bombs
            bombs = int(sysArgs[2])
            if not 0 < bombs <= size * size:
                print(colored("number of bombs must be greater than 0 and cannot exceed number of squares", "red"))
                return
        except:
            print("usage: games.py hangman [size bombs]")
            return 2
    # defaults
    else:
        size = DEFAULT_SIZE
        bombs = DEFAULT_BOMBS

    # need higher recursion limit: https://stackoverflow.com/questions/20034023/maximum-recursion-depth-exceeded-in-comparison
    sys.setrecursionlimit(size * size + 20)

    # set lost variable
    lost = False

    # variable to determine how many flags user has put down, and how many correctly
    flags_correct = 0
    flags_guessed = 0

    # create rows and columns for table
    rows = []
    for i in range(size):
        columns = []
        for j in range(size):
            columns.append(square())
        rows.append(columns)

    # add bombs to table
    i = 0
    while i < bombs:
        # choose where to put bomb
        row = random.randint(0, size - 1)
        column = random.randint(0, size - 1)

        # check whether bomb already there
        if rows[row][column].bomb:
            continue

        # put in bomb
        rows[row][column].bomb = True
        i += 1

        # update squares around bomb
        # left
        if column > 0:
            rows[row][column - 1].nearby += 1

        # right
        if column < size - 1:
            rows[row][column + 1].nearby += 1

        # above
        if row > 0:
            # directly above
            rows[row - 1][column].nearby += 1
            # upper left
            if column > 0:
                rows[row - 1][column - 1].nearby += 1
            # upper right
            if column < size - 1:
                rows[row - 1][column + 1].nearby += 1

        # below
        if row < size - 1:
            # directly below
            rows[row + 1][column].nearby += 1
            # lower left
            if column > 0:
                rows[row + 1][column - 1].nearby += 1
            # lower right
            if column < size - 1:
                rows[row + 1][column + 1].nearby += 1

    # save time to determine game time
    # https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-execution
    start_time = time.time()

    # implement actual gameplay
    while True:
        # print what's been revealed
        print_screen(rows, size, lost, flags_guessed, bombs)
        print()

        # ask for row and column number, plus optional flag
        print(colored("type 'h' for help", "yellow"))
        user_input = get_string("row column [f]: ").split()

        # check user user_input length
        if len(user_input) < 2 or len(user_input) > 3:
            unused_variable = os.system('clear')
            print(colored("\nPlease type in row number followed by a space followed by column number.\nYou may also type 'f' after those to indicate you want to place/remove a flag\nExample: 1 1 f", "red"))
            # https://stackoverflow.com/questions/983354/how-do-i-make-python-to-wait-for-a-pressed-key
            input("Press Enter to continue")
            continue

        # user must user_input (positive) integer for row and column
        if not user_input[0].isdigit() or not user_input[1].isdigit():
            unused_variable = os.system('clear')
            print(colored("row and column numbers must be positive integers", "red"))
            input("Press Enter to continue")
            continue

        # save row and column
        row = int(user_input[0])
        column = int(user_input[1])

        # row/column must be less than size
        if row >= size or column >= size:
            unused_variable = os.system('clear')
            print(colored(f"row and column numbers must be less than {size}", "red"))
            input("Press Enter to continue")
            continue

        # putting down/removing flag, but not in place already revealed
        if len(user_input) == 3 and not rows[row][column].revealed:
            # check for flag request
            if user_input[2] != "f":
                unused_variable = os.system('clear')
                print(colored("third term, if input, must be 'f'", "red"))
                input("Press Enter to continue")
                continue

            # remove flag if there already
            if rows[row][column].flag:
                rows[row][column].flag = False
                # if needed, update correct flags variable
                if rows[row][column].bomb:
                    flags_correct -= 1
                # update total flags placed
                flags_guessed -= 1

            # add flag if not there already
            else:
                rows[row][column].flag = True
                # if needed, update correct flags variable
                if rows[row][column].bomb:
                    flags_correct += 1
                # update total flags placed
                flags_guessed += 1

            # check whether won game
            if flags_correct == flags_guessed == bombs:
                print_screen(rows, size, lost, flags_guessed, bombs)
                print()
                print()
                print(colored("WINNER!", "green"))
                print("--- %s seconds ---" % (time.time() - start_time))
                if helpers.play_again():
                    return minesweeper(sysArgs)
                else:
                    return

            # if user hasn't won, next user_input
            continue

        # cannot reveal under a flag
        if rows[row][column].flag:
            print(colored("remove flag first", "red"))
            time.sleep(3)
            continue

        # update what is revealed and determine whether bomb was selected
        lost = reveal(rows, row, column, size)

        if lost:
            print_screen(rows, size, lost, flags_guessed, bombs)
            print()
            print()
            print(colored("LOSER", "red"))
            if helpers.play_again():
                return minesweeper(sysArgs)
            else:
                return


def reveal(rows, row, column, size):
    """Checks whether user has been bombed; if not, reveals appropriate squares"""

    # it's a bomb!
    if rows[row][column].bomb:
        return True

    # check whether square already revealed
    if rows[row][column].revealed:
        return False

    # reveal square, (unless there's a flag on it – relevant when auto-showing next to 0s)
    if not rows[row][column].flag:
        rows[row][column].revealed = True

    # decide whether squares nearby need to be revealed
    if rows[row][column].nearby != 0:
        return False

    # reveal squares on all sides
    # left
    if column > 0:
        reveal(rows, row, column - 1, size)

    # right
    if column < size - 1:
        reveal(rows, row, column + 1, size)

    # above
    if row > 0:
        # directly above
        reveal(rows, row - 1, column, size)
        # upper left
        if column > 0:
            reveal(rows, row - 1, column - 1, size)
        # upper right
        if column < size - 1:
            reveal(rows, row - 1, column + 1, size)

    # below
    if row < size - 1:
        # directly below
        reveal(rows, row + 1, column, size)
        # lower left
        if column > 0:
            reveal(rows, row + 1, column - 1, size)
        # lower right
        if column < size - 1:
            reveal(rows, row + 1, column + 1, size)

    # all done!
    return False


def print_screen(rows, size, lost, flags_guessed, bombs):
    """Prints screen as discovered by the user, or full screen if game was lost"""

    # clear screen
    unused_variable = os.system('clear')
    print("\12")

    # tell user number of flags placed
    print("\n\n\n")
    print("Flags: " + str(flags_guessed) + "/" + str(bombs))
    print("\n\n")

    # print column heads
    print("    ", end="")
    for column in range(size):
        # print column number
        # single digit
        if column < 10:
            print(column, end="  ")
        # double digit
        else:
            print(column, end=" ")
    print()

    # separate heads from table
    for column in range(size + 1):
        print("___", end="")
    print()

    # print each row
    for row in range(size):
        # print row number
        # single digit
        if row < 10:
            print(row, end="  |")
        # double digit
        else:
            print(row, end=" |")

        # print column within row
        for column in range(size):
            # if revealed or game is over
            if rows[row][column].revealed or lost:
                # print bombs (if lost)
                if rows[row][column].bomb:
                    print(colored("b", "white", "on_red"), end="  ")
                # print 0s
                elif rows[row][column].nearby == 0:
                    print(colored(rows[row][column].nearby, "white", "on_grey"), end="  ")
                # print other numbers
                else:
                    print(colored(rows[row][column].nearby, "cyan", "on_grey"), end="  ")
            # print 'f' if flag placed
            elif rows[row][column].flag:
                print(colored("f", "white", "on_green"), end="  ")
            # otherwise, not revelaled. Print '?'
            else:
                print("?", end="  ")
        print()

if __name__ == "__main__":
    minesweeper(sys.argv)