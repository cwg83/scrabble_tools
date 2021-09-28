import itertools
from collections import defaultdict
import math


# Dictionary of the number of each tile in a bag of Scrabble tiles. Blanks = ?
frequencies = {"E": 12,
               "A": 9, "I": 9,
               "O": 8,
               "N": 6, "R": 6, "T": 6,
               "L": 4, "S": 4, "U": 4, "D": 4,
               "G": 3,
               "?": 2, "B": 2, "C": 2, "M": 2, "P": 2, "F": 2, "H": 2, "V": 2, "W": 2, "Y": 2,
               "K": 1, "J": 1, "X": 1, "Q": 1, "Z": 1}


def is_valid(word):
    with open('NSWL2020.txt') as f:
        found = False
        for line in f:
            words = line.split()
            if words[0] == word:
                found = True
                return True, line
        if not found:
            return False


# Replaces a letter at a specific index of the word with "?" (representing a blank tile)
def replace_with_blank(word, index, replacement):
    return word[:index] + replacement + word[index+1:]


# Returns a list of each variation of the word using a single blank tile
def single_blanks(word):
    single_cases = [replace_with_blank(word, idx, "?") for idx in range(len(word))]
    # It is necessary to sort each variation of the word to account for words with duplicate letters and create a set
    sorted_single = [''.join(sorted(ele)) for ele in single_cases]
    return list(set(sorted_single))


# Returns a list of each variation of the word using two blank tiles
def double_blanks(word):
    double_cases = []
    for idx1, idx2 in itertools.combinations(range(len(word)), 2):
        first_blank = replace_with_blank(word, idx1, "?")
        second_blank = replace_with_blank(first_blank, idx2, "?")
        double_cases.append(second_blank)
    sorted_double = [''.join(sorted(ele)) for ele in double_cases]
    return list(set(sorted_double))


# Returns the combination of both the single_blanks and double_blanks lists + the word itself
def all_blanks(word):
    return list(set([word] + single_blanks(word) + double_blanks(word)))


# Cases will be the result of all_blanks, which is a list of all possible variations of the word, including blanks
# Only works for 7-letter words currently
def probability(cases):
    numerators = []
    for case in cases:
        numerator = 1
        # The denominator will always be C(100, 7)
        denominator = 16007560800
        # Count of the characters in each case
        char_count = defaultdict(int)
        char_combinations = []
        for character in case:
            char_count[character] += 1
        # Calculate the total combinations of each character count using n! / r! * (n - r)!
        for key in char_count:
            # n = the count of the character in the bag of tiles, r = the count of the character in the case
            n = frequencies[key]
            r = char_count[key]
            num = math.factorial(n) / (math.factorial(r) * math.factorial(n - r))
            char_combinations += [num]
        # Add the result to the numerators list
        for combination in char_combinations:
            numerator = numerator * combination
        numerators += [numerator]
    total_numerators = sum(numerators)
    total_probability = (total_numerators / denominator) * 100
    return total_probability


# Function to create a ranked list of the probabilities of words of a certain length.
# Only works for 7-letter words currently
def probability_of_all(word_length, number_to_display):
    prob_dict = {}
    with open('NSWL2020.txt') as f:
        for line in f:
            words = line.split()
            if len(words[0]) == word_length:
                try:
                    prob_dict[words[0]] = probability(all_blanks(words[0]))
                except ValueError:
                    pass
    sorted_probabilities = dict(sorted(prob_dict.items(), key=lambda item: item[1], reverse=True))
    for key, value in list(sorted_probabilities.items())[:number_to_display]:
        print(key, value)


if __name__ == "__main__":
    word_to_check = input("Word to check: ").upper()
    probability_to_check = "".join(word_to_check)
    if not is_valid(word_to_check):
        print("This is not a valid Scrabble word.")
    else:
        print(is_valid(word_to_check)[1].strip())
        print("Probability: " + str(probability(all_blanks(probability_to_check))))
    while True:
        probability_list = input("Would you like to see a list of the most probable 7-letter words? (Y or N)").upper()
        if probability_list == "N":
            break
        if probability_list == "Y":
            while True:
                try:
                    list_length = int(input("List length: (between 10 and 1000)"))
                except ValueError:
                    print("Please enter a valid integer")
                    continue
                else:
                    if list_length < 10 or list_length > 1000:
                        print("Please enter a list length from 10 to 1000")
                        continue
                    else:
                        probability_of_all(7, list_length)
                        break
        else:
            print("Please type Y or N")
            continue

