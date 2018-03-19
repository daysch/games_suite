# Plays hangman in terminal window

# libraries to import
from cs50 import get_string
from cs50 import get_float
from cs50 import get_char
import os
import sys
import time
import random
import string
import webbrowser
import helpers
import time


MAX_MISTAKES = 7
DEFAULT_DICTIONARY = "dictionary"


def hangman():
    # suppress traceback
    sys.tracebacklimit = 0

    # clear screen
    unused_variable = os.system('clear')
    print("\12")

    # check for user-inputted dictionary
    if len(sys.argv) == 3:
        chosen_dictionary = sys.argv[2]
    else:
        chosen_dictionary = DEFAULT_DICTIONARY

    # open dictionary
    try:
        dictionary = open(chosen_dictionary).read().splitlines()
    except:
        print("COULD NOT LOAD DICTIONARY")
        return 2

    # get number of players from user
    while True:
        # clear screen
        unused_variable = os.system('clear')
        print("\12")

        # get number of players
        players = get_float("1 or 2 players?\n")

        # for one player, computer chooses word
        if players == 1:
            word = decide_word(dictionary)
            break
        # for two players, user chooses word
        elif players == 2:
            word = get_word(dictionary)
            break
        # easter egg!!!
        elif players == 3.141592654:
            print("YUMMY!")
            time.sleep(1)
            webbrowser.open("http://www.easteregg.com/", new=2)
            if helpers.play_again():
                return hangman()
            else:
                return

    # set up for guessing
    revealed_word = "_" * len(word)
    mistakes = 0
    already_guessed = []
    letters_left = list(string.ascii_lowercase)

    # https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-execution
    start_time = time.time()

    # get letter one at a time until word is guessed or reached max number of mistakes
    while mistakes < MAX_MISTAKES:
        # clear screen
        unused_variable = os.system('clear')

        # show user how many mistakes left
        print(f"MISTAKES LEFT: {MAX_MISTAKES - mistakes}")

        # print letters left
        print()
        for letters in letters_left:
            print(letters, end=" ")
        print("\n\n\n")

        # print word as figured out so far
        for letters in revealed_word:
            print(letters, end=" ")
        print("\n\n")

        # get letter (or word guess) from user
        guess = get_string("Guess: ")

        # ensure word is only lower case letters
        if not guess.islower():
            print("LOWERCASE LETTERS ONLY")
            time.sleep(1)
            continue

        # ensure letter/word hasn't already been guessed
        if guess in already_guessed:
            print("ALREADY GUESSED")
            time.sleep(1)
            continue

        # if word guess, check
        if len(guess) != 1:
            # if correct, they won
            if guess == word:
                # clear screen
                unused_variable = os.system('clear')

                # tell user they've won
                print(f"MISTAKES LEFT: {MAX_MISTAKES - mistakes}")
                for letters in word:
                    print(letters, end=" ")
                print("\nWINNER")
                print("--- %s seconds ---" % (time.time() - start_time))
                # ask user to play again
                if helpers.play_again():
                    return hangman()
                else:
                    return

            # otherwise, they made a mistake!
            mistakes += 1
            already_guessed.append(guess)
            continue

        # if not word guess, check letter
        if guess in word:
            # save that we've found the letter for all instances in word
            for i, letters in enumerate(word):
                if letters == guess:
                    revealed_word = revealed_word[:i] + guess + revealed_word[i + 1:]
            letters_left.remove(guess)
            already_guessed.append(guess)

            # check whether game has been won
            if word == revealed_word:
                # clear screen
                unused_variable = os.system('clear')

                # tell user they've won
                print(f"MISTAKES LEFT: {MAX_MISTAKES - mistakes}")
                for letters in word:
                    print(letters, end=" ")
                print("\nWINNER")
                print("--- %s seconds ---" % (time.time() - start_time))
                # ask user to play again
                if helpers.play_again():
                    return hangman()
                else:
                    return

            # get next guess
            continue

        # if letter not in word, mistake!
        mistakes += 1
        letters_left.remove(guess)
        already_guessed.append(guess)

    # if reached this point, user has lost!
    print("\nLOSER\nAnswer: " + word)

    # ask user to play again
    if helpers.play_again():
        return hangman()
    else:
        return


def get_word(dictionary):
    """Get valid word contained in dictionary from user"""

    while True:
        # clear screen
        unused_variable = os.system('clear')

        # prompt user for word
        word = get_string("Word: ")

        # word must be all lowercase letters
        if not word.islower() or not word.isalpha():
            print("MUST BE LOWERCASE WORD WITHOUT PUNCTUATION")
            time.sleep(1)
            continue

        # make sure actually a word
        if word in dictionary:
            break
        print("WORD NOT IN DICTIONARY")
        time.sleep(1)

    # clear screen
    unused_variable = os.system('clear')
    print("\12")

    return word


def decide_word(dictionary):
    """Randomly choose word in dictionary"""

    # get random word from dictionary until word is valid
    while True:
        word = random.choice(dictionary)
        if word.isalpha() and word.islower():
            return word


if __name__ == "__main__":
    hangman()
