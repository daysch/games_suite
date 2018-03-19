from cs50 import get_char
import os


def play_again():
    """Asks user to play again"""
    while True:
        # prompt user
        answer = get_char("Play again? (y/n): ")
        if answer == "y":
            return True
        if answer == "n":
            return False

        # clear screen
        unused_variable = os.system('clear')