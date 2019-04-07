import os

def get_words(filepath):
    words = []
    with open(filepath, 'r') as f:
        for line in f:
            words.append(line.strip())
    return words

def get_letter_sets(words):
    letter_sets = dict()
    for word in words:
        letter_sets[word] = set(word)
    return letter_sets

def get_possible_words(letter_sets, n_letters, letters):
    for word, letter_set in letter_sets.items():
        if len(word) == n_letters and letter_set.issubset(letters):
            print(word)


words = get_words(os.path.join('word_lists', 'CROSSWD.TXT'))
letter_sets = get_letter_sets(words)

n_letters = 8
letters = set('cfieetstegtl')

get_possible_words(letter_sets, n_letters, letters)