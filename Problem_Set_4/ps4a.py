# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    permutations = []

    def insert(sequence, letter):
        poss = []
        for i in range(len(sequence) + 1):
            temp = sequence[:i] + letter + sequence[i:]
            poss.append(temp)
        return poss

    if len(sequence) == 1:
        permutations.append(sequence)
        return permutations

    else:
        reduced = get_permutations(sequence[1:])
        for item in reduced:
            permutations += insert(item, sequence[0])
            permutations.sort()

    return permutations

if __name__ == '__main__':
    
    test_1 = 'car'
    print('------------Test 1------------')
    print('Input:', test_1)
    print('Expected Output:', ['acr', 'arc', 'car', 'cra', 'rac', 'rca'])
    print('Actual Output:', get_permutations('car'))
    
    test_2 = 'mat'
    print('------------Test 2------------')
    print('Input:', test_2)
    print('Expected Output:', ['amt', 'atm', 'mat', 'mta', 'tam', 'tma'])
    print('Actual Output:', get_permutations('mat'))

    test_3 = 'ac'
    print('------------Test 3------------')
    print('Input:', test_3)
    print('Expected Output:', ['ac', 'ca'])
    print('Actual Output:', get_permutations('ac'))
