# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string
import copy #for the deep copy version of subsitute_hand()

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*': 0
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

# WORDLIST_FILENAME = "words.txt"
WORDLIST_FILENAME = "Problem_Set_3/words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    # print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    # print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    # print(word)
    word = word.lower()
    # print(word)
    first_comp = 0
    for char in word:
        first_comp += SCRABBLE_LETTER_VALUES[char]
        # print(char, SCRABBLE_LETTER_VALUES[char], first_comp)
    val = ((7 * len(word)) - (3 * (n - len(word))))
    second_comp = max(1, val)
    # print(val, second_comp)
    score = first_comp * second_comp
    # print(score)
    return score

    # pass  # TO DO... Remove this line when you implement this function

# print(get_word_score("WEED", 6))

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end = ' ')      # print all on the same line
    print()                              # print an empty line


# display_hand({'a':1, 'x':2, 'l':3, 'e':1})
#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand = {'*': 1}
    num_vowels = int(math.ceil(n / 3)) - 1

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n - 1):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

# print(deal_hand(7))
#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    # new_hand = hand
    # for char in word.lower():
    #     if char in hand.keys():
    #         new_hand[char] = hand.get(char, 0) - 1
    #     else:

    # for char in hand.keys():
    #     if char in word.lower():
    #         # if hand[char] > 0:
    #         new_hand[char] = hand.get(char, 0) - 1
    #         print(char, new_hand)
    #     else:
    #         new_hand[char] = hand.get(char, 0)
    #         print(char, new_hand)
    #     if new_hand[char] == 0:
    #             new_hand.pop(char)
    # return new_hand
    new_hand = {}
    word_dict = get_frequency_dict(word.lower())
    for char in hand.keys():
        if char in word_dict.keys():
            avai = hand.get(char, 0) - word_dict.get(char, 0)
            new_hand[char] = max(avai, 0)
        else:
            new_hand[char] = hand.get(char, 0)
        if new_hand[char] == 0:
            new_hand.pop(char)
    return new_hand

# print(update_hand({'a':1, 'x':2, 'l':3, 'e':1}, "axmley"))
# print(update_hand({'a': 1, 'q': 1, 'l': 2, 'm': 1, 'u': 1, 'i': 1}, 'quail'))
# print(update_hand({'e': 1, 'v': 2, 'n': 1, 'i': 1, 'l': 2}, 'Evil'))
# print(update_hand({'*': 1, 'e': 1, 'o': 1, 'g': 2, 'x': 1, 'q': 1}, 'qeo'))


#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    word_dict = get_frequency_dict(word.lower())
    # temp_word = ""
    # print(word_dict)
    for char in word_dict.keys():
        # print(char, word_dict.get(char, 0), hand.get(char, 0))
        # if word_dict.get(char, 0) <= hand.get(char, 0) and word.lower() in word_list:
        if word_dict.get(char, 0) > hand.get(char, 0):
            return False

    if "*" not in word.lower() and word.lower() in word_list:
        return True
    elif "*" in word:
        for vowel in VOWELS:
            temp_word = word.lower().replace('*', vowel)
            # print(temp_word)
            if temp_word in word_list:
                return True
        

# print(is_valid_word('excruciating', {'e': 1, 'v': 2, 'n': 1, 'i': 1, 'l': 2}, load_words()))
# print(is_valid_word('Honey', {'h': 1, 'e': 2, 'n': 1, 'y': 1, 'o': 2}, load_words()))
#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    length = 0
    for char in hand.keys():
        length += hand.get(char, 0)
    return length
    # pass  # TO DO... Remove this line when you implement this function

# print(calculate_handlen({'e': 1, 'v': 2, 'n': 1, 'i': 1, 'l': 2}))

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    total_score = 0

    while len(hand) > 0:
        print('\n')
        print("Current Hand:", end = ' ')
        display_hand(hand)
        word = input('Enter word or "!!" to indicate that you are finished: ').lower()
        if word == "!!":
            print("Total Score for this hand:", total_score)
            print("----------")
            break
        else:
            if is_valid_word(word, hand, word_list):
                hand_length = calculate_handlen(hand)
                word_points = get_word_score(word, hand_length)
                total_score += word_points
                print('"%s" earned %d points. Total: %d points' % (word, word_points, total_score))
                # print('\n')
            else:
                print("That is not a valid word. Please choose another word.")
            hand = update_hand(hand, word)
    
    if len(hand) == 0:
        print('\n')
        print("Ran out of letters." + "\n" + "Total score for this hand:", total_score)
        print("----------")
    return total_score

    
    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function
    # Keep track of the total score
    
    # As long as there are still letters left in the hand:
    
        # Display the hand
        
        # Ask user for input
        
        # If the input is two exclamation points:
        
            # End the game (break out of the loop)

            
        # Otherwise (the input is not two exclamation points):

            # If the word is valid:

                # Tell the user how many points the word earned,
                # and the updated total score

            # Otherwise (the word is not valid):
                # Reject invalid word (print a message)
                
            # update the user's hand by removing the letters of their inputted word
    

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score

    # Return the total score as result of function

# play_hand({'h': 1, 'e': 2, 'l': 2, 'y': 1, 'm': 2, '*': 1}, load_words())

#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    ## Misinterpreted version of question, where performing as many separate random replacements as the value of
    ## letter being replaced. Used deepcopy here as workaround.

    # amount = hand.get(letter, 0)
    # # print(hand)
    # new_hand = copy.deepcopy(hand)
    # # print(amount, new_hand)
    # if letter in hand.keys():
    #     new_hand.pop(letter)
    #     # print(hand)
    #     while amount > 0:
    #         substitute_letter = random.choice(VOWELS + CONSONANTS)
    #         if substitute_letter not in hand.keys() and substitute_letter != letter:
    #             new_hand[substitute_letter] = new_hand.get(substitute_letter, 0) + 1
    #             amount -= 1
    #             # print(substitute_letter, new_hand)
    # return new_hand

    ## Solved properly using for loop. 

    new_hand = {}

    if letter not in hand:
        return hand
    
    for char in hand.keys():
        if char != letter:
            new_hand[char] = hand.get(char, 0)
        else:
            substitute_letter = random.choice(VOWELS + CONSONANTS)
            while substitute_letter in hand.keys():
                substitute_letter = random.choice(VOWELS + CONSONANTS)
            new_hand[substitute_letter] = hand.get(letter, 0)

    return new_hand

    
    # pass  # TO DO... Remove this line when you implement this function
       
print(substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l'))
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    hands = int(input("Enter total number of hands: "))
    series_score = 0
    substitutes_left = 1
    replays_left = 1

    while hands > 0:
        hand = deal_hand(HAND_SIZE)
        print("Current Hand:", end = ' ')
        display_hand(hand)
    
        if substitutes_left > 0:
            to_substitue = input("Would you like to substitute a letter: ").lower()
            if to_substitue == "yes":
                letter = input("Which letter would you like to replace: ").lower()
                hand = substitute_hand(hand, letter)
                substitutes_left -= 1

        score_1 = play_hand(hand, word_list)
        score_2 = 0

        if replays_left > 0:
            to_replay = input("Would you like to replay the hand: ").lower()
            if to_replay == "yes":
                score_2 = play_hand(hand, word_list)
                replays_left -= 1

        series_score += max(score_1, score_2)
        hands -= 1

    print("Total score over all hands:", series_score)


    # print("play_game not implemented.") # TO DO... Remove this line when you implement this function
    
# play_game(load_words())

#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
# #
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
