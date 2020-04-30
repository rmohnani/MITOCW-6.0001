# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

# WORDLIST_FILENAME = "words.txt"
WORDLIST_FILENAME = "Problem Set 2/words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    for char in secret_word:
      # print(char)
      if  char not in letters_guessed:
        # print('false')
        return False   
    else:
      # print('true')
      return True
    # pass

# is_word_guessed('hello', ['h', 'r', 'e', 'l', 'k', 'm', 'o'])


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    guessed = ""
    for char in secret_word:
      if char in letters_guessed:
        guessed += char + " "
        # print(guessed)
      else:
        guessed += "_ "
    return guessed
    # pass

# get_guessed_word('hello', ['i', 'r', 'j', 'b', 'k', 'm', 'o'])

def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    letters = string.ascii_lowercase
    letters_left = ""
    for char in letters:
      # print(char)
      if char not in letters_guessed:
        letters_left += char
        # print(letters_left)
    return letters_left
    # print(letters_left)
    # print(len(letters_left))
    # pass
    
# get_available_letters(['i', 'r', 'j', 'b', 'k', 'm', 'o'])

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is", len(secret_word), "letters long")
    # print("Only enter letters. If you do not enter letters you will lose a warning and if you do not have any warnings left you will lose a guess")
    print("You have 3 warnings left")
    print("-------------")


    warnings_left = 3
    guesses_left = 6
    letters_guessed = []
    consonants = "bcdfghjklmnpqrstvwxyz"
    vowels = "aeiou"

    while guesses_left > 0 and is_word_guessed(secret_word, letters_guessed) == False:
      # print("You have", warnings_left, "warnings left")
      print("You have", guesses_left, "guesses left")
      print("Available letters:", get_available_letters(letters_guessed))
      # print(letters_guessed)
      guess = input("Please guess a letter: ").lower()

      # if guess.isalpha() is False or guess in letters_guessed:
      #   if guess.isalpha() is False:
      #     print("You can only enter an alphabet.")
      #   else:
      #     print("You cannot enter a letter you have already guessed.")
      #   if warnings_left == 0:
      #     guesses_left -= 1
      #   else:
      #     warnings_left -= 1

      # display = get_guessed_word(secret_word, letters_guessed)
      if guess in secret_word and guess not in letters_guessed:
        letters_guessed.append(guess)
        display = get_guessed_word(secret_word, letters_guessed)
        print("Good guess:", display)
      elif guess.isalpha() is False:
        if warnings_left > 0:
          warnings_left -= 1
          print("Oops! That is not a valid letter. You have", warnings_left, "warnings left:", display)
        else:
          guesses_left -= 1
          print("Oops! That is not a valid letter. You have no warnings left, so you lose one guess:", display)
      elif guess.isalpha() is True and guess in letters_guessed:
        if warnings_left > 0:
          warnings_left -= 1
          print("Oops! You've already guessed that letter. You have", warnings_left, "warnings left:", display)
        else:
          guesses_left -= 1
          print("Oops! You've already guessed that letter. You have no warnings left, so you lose one guess:", display)
      elif guess.isalpha() is True and guess not in letters_guessed and guess in consonants:
        letters_guessed.append(guess)
        display = get_guessed_word(secret_word, letters_guessed)
        print("Oops! That letter is not in my word:", display)
        guesses_left -= 1
      elif guess.isalpha() is True and guess not in letters_guessed and guess in vowels:
        letters_guessed.append(guess)
        display = get_guessed_word(secret_word, letters_guessed)
        print("Oops! That letter is not in my word:", display)
        guesses_left -= 2
      print("-------------")
    # pass
    if is_word_guessed(secret_word, letters_guessed) == True:
      print("Congratulations, you won!")
      # print(set(secret_word))
      total_score = guesses_left * len(set(secret_word))
      # print(total_score)
      print("Your total score for this game is:", total_score)
    elif guesses_left == 0 and is_word_guessed(secret_word, letters_guessed) == False:
      print("Sorry, you ran out of guesses. The word was", secret_word)

# hangman("hello")

# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    # print(my_word)
    my_word = my_word.replace(" ", "")
    # print(my_word)
    if len(my_word) != len(other_word):
      return False
    for i in range(len(my_word)):
      # print(my_word[i], other_word[i])
      if my_word[i].isalpha() == True and other_word[i].isalpha() == True and my_word[i] != other_word[i]:
        # print(my_word[i], other_word[i])
        return False
    return True
    # pass

# print(match_with_gaps('t _ _ t', 'tact'))


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    matches = ""
    for word in wordlist:
      if match_with_gaps(my_word, word) == True:
        matches += word + " "
    if matches == "":
      print("No matches found.")
    return matches
    # print(matches)
    # pass

# show_possible_matches("t _ _ t")

def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is", len(secret_word), "letters long")
    # print("Only enter letters. If you do not enter letters you will lose a warning and if you do not have any warnings left you will lose a guess")
    print("You have 3 warnings left")
    print("-------------")


    warnings_left = 3
    guesses_left = 6
    letters_guessed = []
    consonants = "bcdfghjklmnpqrstvwxyz"
    vowels = "aeiou"

    while guesses_left > 0 and is_word_guessed(secret_word, letters_guessed) == False:
      # print("You have", warnings_left, "warnings left")
      print("You have", guesses_left, "guesses left")
      print("Available letters:", get_available_letters(letters_guessed))
      # print(letters_guessed)
      guess = input("Please guess a letter: ").lower()

      # if guess.isalpha() is False or guess in letters_guessed:
      #   if guess.isalpha() is False:
      #     print("You can only enter an alphabet.")
      #   else:
      #     print("You cannot enter a letter you have already guessed.")
      #   if warnings_left == 0:
      #     guesses_left -= 1
      #   else:
      #     warnings_left -= 1

      # display = get_guessed_word(secret_word, letters_guessed)
      if guess in secret_word and guess not in letters_guessed:
        letters_guessed.append(guess)
        display = get_guessed_word(secret_word, letters_guessed)
        print("Good guess:", display)
      elif guess.isalpha() is False and guess != "*":
        if warnings_left > 0:
          warnings_left -= 1
          print("Oops! That is not a valid letter. You have", warnings_left, "warnings left:", display)
        else:
          guesses_left -= 1
          print("Oops! That is not a valid letter. You have no warnings left, so you lose one guess:", display)
      elif guess.isalpha() is True and guess in letters_guessed:
        if warnings_left > 0:
          warnings_left -= 1
          print("Oops! You've already guessed that letter. You have", warnings_left, "warnings left:", display)
        else:
          guesses_left -= 1
          print("Oops! You've already guessed that letter. You have no warnings left, so you lose one guess:", display)
      elif guess.isalpha() is True and guess not in letters_guessed and guess in consonants:
        letters_guessed.append(guess)
        display = get_guessed_word(secret_word, letters_guessed)
        print("Oops! That letter is not in my word:", display)
        guesses_left -= 1
      elif guess.isalpha() is True and guess not in letters_guessed and guess in vowels:
        letters_guessed.append(guess)
        display = get_guessed_word(secret_word, letters_guessed)
        print("Oops! That letter is not in my word:", display)
        guesses_left -= 2
      elif guess == "*":
        print("Possible matches are:", show_possible_matches(display))
      print("-------------")
    # pass
    if is_word_guessed(secret_word, letters_guessed) == True:
      print("Congratulations, you won!")
      # print(set(secret_word))
      total_score = guesses_left * len(set(secret_word))
      # print(total_score)
      print("Your total score for this game is:", total_score)
    elif guesses_left == 0 and is_word_guessed(secret_word, letters_guessed) == False:
      print("Sorry, you ran out of guesses. The word was", secret_word)

    # pass



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
