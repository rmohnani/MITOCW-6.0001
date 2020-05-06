# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string
import copy

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("Problem_Set_4/story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'Problem_Set_4/words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object

        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class

        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.

        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.

        shift (integer): the amount by which to shift every letter of the
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to
                 another letter (string).
        '''
        shift_dict = {}
        assert 0 <= shift < 26, "Shift value not in range 0 to 25 inclusive."
        lowercase = string.ascii_lowercase

        for i in range(len(lowercase)):
            if i + shift <= 25:
                shift_dict[lowercase[i]] = lowercase[i + shift]
            else:
                shift_dict[lowercase[i]] = lowercase[i + shift - 26]
        
        # Instead of repeating same process above for uppercase, decided to simply take the existing 
        # lowercase key-value pairs in the dictionary and add uppercase versions to the dictionary

        for item in list(shift_dict):
            shift_dict[item.upper()] = shift_dict[item].upper()

        return shift_dict

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift

        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        shift_dict = self.build_shift_dict(shift)
        shifted = ""

        for char in self.message_text:
            if char in shift_dict:
                shifted += shift_dict[char]
            else:
                shifted += char

        return shifted

    def __str__(self):
        return self.message_text

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object

        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(self.shift)
        self.message_text_encrypted = self.apply_shift(self.shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class

        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class

        Returns: a COPY of self.encryption_dict
        '''
        return copy.deepcopy(self.encryption_dict)

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class

        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other
        attributes determined by shift.

        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        assert 0 <= shift < 26, "Shift value not in range 0 to 25 inclusive."
        self.__init__(self.message_text, shift)

    def __str__(self):
        return self.message_text + "," + str(self.shift) + "," + self.message_text_encrypted

class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object

        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create
        the maximum number of valid words, you may choose any of those shifts
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        # ### Initial Implementation through using a dictionary

        # all_dict = {}
        # for s in range(26):
        #     decrypted = self.apply_shift(s)
        #     words = decrypted.split(" ")
        #     count = 0
        #     for item in words:
        #         if is_word(self.valid_words, item):
        #             count += 1
        #         all_dict[26 - s] = (decrypted, count)

        # max_valid_words = 0
        # decrypted_message = ""
        # best_shift_value = ""

        # for poss in all_dict.items():
        #     if poss[1][1] > max_valid_words:
        #         decrypted_message = poss[1][0]
        #         max_valid_words = poss[1][1]
        #         best_shift_value = poss[0]

        # return (best_shift_value, decrypted_message)

        ### More efficient implementation just using trackers
        max_valid_words = 0
        decrypted_message = ""
        best_shift_value = ""

        for s in range(26):
            decrypted = self.apply_shift(s)
            words = decrypted.split(" ")
            count = 0
            for item in words:
                if is_word(self.valid_words, item):
                    count += 1
            if count > max_valid_words:
                decrypted_message = decrypted
                max_valid_words = count
                best_shift_value = 26 - s

        return (best_shift_value, decrypted_message)

    def __str__(self):
        return self.message_text

if __name__ == '__main__':

   #Example test case (PlaintextMessage)
    plaintext1 = PlaintextMessage('hello', 2)
    print('Expected Output: jgnnq')
    print('Actual Output:', plaintext1.get_message_text_encrypted())

   #Example test case (CiphertextMessage)
    ciphertext1 = CiphertextMessage('jgnnq')
    print('Expected Output:', (2, 'hello'))
    print('Actual Output:', ciphertext1.decrypt_message())

    #TODO: WRITE YOUR TEST CASES HERE

    plaintext2 = PlaintextMessage('everybody is Home!', 7)
    print('Expected Output: lclyfivkf pz Ovtl!')
    print('Actual Output:', plaintext2.get_message_text_encrypted())

    plaintext3 = PlaintextMessage('Good morning.', 13)
    print('Expected Output: Tbbq zbeavat.')
    print('Actual Output:', plaintext3.get_message_text_encrypted())

    ciphertext2 = CiphertextMessage('mubb tedu')
    print('Expected Output:', (16, 'well done'))
    print('Actual Output:', ciphertext2.decrypt_message())

    ciphertext3 = CiphertextMessage('Gdaz wzajmz Yzvoc. Nomziboc wzajmz Rzvfiznn. Ejpmizt wzajmz Yznodivodji.')
    print('Expected Output:', (21, 'Life before Death. Strength before Weakness. Journey before Destination.'))
    print('Actual Output:', ciphertext3.decrypt_message())

    #TODO: best shift value and unencrypted story
    story = CiphertextMessage(get_story_string())
    print(story.decrypt_message())
    """(14, 'Jack Florey is a mythical character created on the spur of a moment to 
    help cover an insufficiently planned hack. He has been registered for classes at
    MIT twice before, but has reportedly never passed aclass. It has been the tradition
    of the residents of East Campus to become Jack Florey for a few nights each year 
    to educate incoming students in the ways, means, and ethics of hacking.')"""
