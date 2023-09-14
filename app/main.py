"""
Hangman Game Backend

This module implements the backend logic for a Hangman game. It manages the game state,
player guesses, and provides methods for interacting with the game
including the change of language from german to english.

Usage:
1. Gives the player the ability to choose between english or german.
2. Initialize a new game with a secret word.
3. Allow players to guess letters with limited tries.
4. Check game status and outcomes.
5. Displays the hangman figure slowely being "Hanged".

Author: Erion Haziri
"""


import random


# Ich habe diese Farbeinstellung-Stringpalette auf StackOverflow gefunden
# Quelle:
# https://stackoverflow.com/questions/8924173/how-can-i-print-bold-text-in-python
#
# Disable the "too-few-public-methods" warning for this class
# # pylint: disable=too-few-public-methods
class Farbe:
    """
        A class for ANSI escape codes used in text color formatting.
    """
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


ASCII_TITEL = r'''
 _
| |
| |__   __ _ _ __   __ _ _ __ ___   __ _ _ __
| '_ \ / _` | '_ \ / _` | '_ ` _ \ / _` | '_ \
| | | | (_| | | | | (_| | | | | | | (_| | | | |
|_| |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                    __/ |
                   |___/
                                      by ©Erion
'''

print(Farbe.GREEN + ASCII_TITEL + Farbe.END)

print(Farbe.RED + 'Hello, User!' + Farbe.END)


def wahlsprache():
    """
        Displays a menu for language selection and returns the chosen language file.

        Returns:
            str: The chosen language file that will be used for selecting words in the game.
    """
    print(Farbe.DARKCYAN + "Let's play Hangman!\n" + Farbe.END)
    print("In this game you have to try to guess a secret word!\n"
          + "Careful you only have limited tries to find it out!")
    print(Farbe.RED + "Hint! " + Farbe.END + "T.he words are made out of "
          + Farbe.CYAN + "nouns" + Farbe.END + ", "
          + Farbe.CYAN + "verbs" + Farbe.END + " and "
          + Farbe.CYAN + "adjectives" + Farbe.END + "!")

    print("Choose a " + Farbe.YELLOW + "language" + Farbe.END + " for the words:")
    print("Type 1. for " + Farbe.YELLOW + "English" + Farbe.END)
    print("Type 2. for " + Farbe.YELLOW + "German" + Farbe.END)
    wahl = input("Enter the " + Farbe.GREEN + "number" + Farbe.END + " for your choice:\n")
    return {
        "1": "English",
        "2": "German"
    }.get(wahl, "English")
    # Default Wahl der Sprache ist auf English gestellt.
    # Dies passiert wenn keine Antwort gegeben wird.


def auswahlwort(sprache):
    """
        Selects a random word from a language-specific word list.

        Args:
            sprache (str): The language for which to select a word.

        Returns:
            str: A randomly chosen word from the specified language's word list.
    """
    wort_listen = {
        "English": "english.txt",
        "German": "german.txt",
    }
    wort_liste = []
    with open(wort_listen[sprache], "r", encoding="utf-8") as file:
        for line in file:
            wort_liste.append(line.strip())
    return random.choice(wort_liste)


def hangman():
    """
        Implements a Hangman game where the player guesses letters to reveal a secret word.

        The player has a limited number of guesses to fill in the letters of the secret word.
        If the player guesses all the letters correctly within the allowed guesses, they win.
        Otherwise, the player loses.

        The function interacts with the user through the console, displaying the progress of
        the word and providing feedback on each guess.

        This function relies on the 'wahlsprache' and 'auswahlwort' functions to select the
        language and the hidden word to guess.
    """
    vermutungen = 0
    sprache = wahlsprache()
    wort = auswahlwort(sprache)
    wort_liste = list(wort)
    leere_liste = ['_'] * len(wort)
    vermutung_liste = []

    while vermutungen < 7:
        print(" ".join(leere_liste))
        vermutung = input(Farbe.BLUE + "Guess a Letter: " + Farbe.END).lower()

        if len(vermutung) != 1:
            print(Farbe.RED + "Please enter only a single letter!" + Farbe.END)
            continue

        if vermutung == " ":
            print(Farbe.RED + "You cannot use space!" + Farbe.END)
            continue

        if not vermutung.isalpha():
            print(Farbe.RED + "You cannot use numbers or special characters!" + Farbe.END)
            continue

        if vermutung in vermutung_liste:
            print(Farbe.RED + "You cannot guess the same letter twice!" + Farbe.END)
            print("Guessed letters: " + Farbe.RED + str(vermutung_liste) + Farbe.END)
            continue

        vermutung_liste.append(vermutung)
        if vermutung in wort_liste:
            for i, buchstabe in enumerate(wort_liste):
                if buchstabe == vermutung:
                    leere_liste[i] = vermutung

        else:
            vermutungen += 1
            print_hangman(vermutungen)

        if "_" not in leere_liste:
            print(Farbe.GREEN + "Congrats! you win! " + Farbe.END
                  + "The correct word was: ", Farbe.CYAN + wort + Farbe.END)
            break
    else:
        print(Farbe.RED + "You lose! " + Farbe.END
              + "The correct word was: ", Farbe.CYAN + wort + Farbe.END)


def print_hangman(vermutungen):
    """
        Prints the Hangman ASCII art based on the number of incorrect guesses.

        Args:
            vermutungen (int): The number of incorrect guesses made by the player.
    """
    hangmanascii = [
        "+=====∞===",
        "|/    |",
        "|    (_)",
        r"|    \|/",
        "|     |",
        r"|    / \\",
        "8----------"
    ]
    for i in range(vermutungen):
        print(Farbe.PURPLE + hangmanascii[i] + Farbe.END)


hangman()
