### Bubble sort

### where comparing two elements next to each other and comapring values
### if one is bigger than the other then move it to the right and repeat this process
### for every pair of elements in the list

def bubble_sort(unsorted_list):
    # Setting up flag checking if i haven't swapped 
    havent_swapped = False
    # while havent_swapped is false, run this
    while not havent_swapped:                               ### O(n)                    
        # saying it is trie that I haven't swapped yet
        havent_swapped = True       
        for i in range(1, len(unsorted_list)):              ### O(n)
            if unsorted_list[i - 1] > unsorted_list[i]:
                # If left > right, then I am swapping, so havent_swapped = False, so will run while loop again
                havent_swapped = False      
                temp = unsorted_list[i - 1]
                unsorted_list[i - 1] = unsorted_list[i]
                unsorted_list[i] = temp
    # unsorted_list is now sorted since modifying the unsorted list as going along, so returns sorted list.
    return unsorted_list 

# l = [3,7,9,1,4]
# print(bubble_sort(l))

### O(n^2), where n = len(unsorted_list)



### Selection Sort

### Where look at the first element and compare with every other element in list to find smallest
### then put the smallest in the front of the list and repeat process for the remaining elements
### of the list, ie list[1:].

def selection_sort(l):
    sorted_count = 0
    while sorted_count != len(l):               ### looping n time -> O(n)
        for i in range(sorted_count, len(l)):   ### looping (n - sorted_count) times -> O(n)
            if l[i] < l[sorted_count]:
                l[i], l[sorted_count] = l[sorted_count], l[i]
        sorted_count += 1
    return l

# print(selection_sort(l))

### O(n^2), where n = len(l)



### Merge Sort

### Divide and conquer. Breaking the unsorted list into two lists and so on until the len(smallest lists) = 1 or 0
### Sort the smallest lists then merge together two smallest lists comparing the smallest element of each list
### to for a bigger sorted list. Repeat process back up until we get to the original list that is now sorted.

def merge(left, right):
    result = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    while i < len(left):
        result.append(left[i])
        i += 1
    while j < len(right):
        result.append(right[j])
        j += 1
    # print("merge: " + str(left) + "&" + str(right))
    return result


## compare only the smallest element in each sublist
## O(len(left) + len(right)) copied elements
## O(len(longer list)) comparisons
## O(n) -> linear in length of lists


def merge_sort(L):
    # print("merge sort: " + str(L))
    if len(L) < 2:
        return L[:]
    else:
        middle = len(L) // 2
        left = merge_sort(L[:middle])
        right = merge_sort(L[middle:])
        # print(left, right)
        return merge(left, right)

l = [1,3,6,7,2,6,25,18,13]
print(merge_sort(l))

## does log n iterations with order n work at each step

### Overall complexity is O(n log n) -> log-linear complexity


