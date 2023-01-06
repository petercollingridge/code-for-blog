from collections import Counter, defaultdict
from random import shuffle
from utils import get_words


def get_letter_mapping(all_words):
    """
    Get a dictionary that maps a position and letter to a set of words with that letter at that position
    e.g. (0, 'a') => all words beginning with 'a'.
    """
    mapping = defaultdict(set)

    for word in all_words:
        mapping[(0, word[0])].add(word)
        mapping[(2, word[2])].add(word)
        mapping[(4, word[4])].add(word)

    return mapping


def get_intersecting_words(mapping, word, position):
    """
    Given a word anf the position it is in (0, 2 or 4 for top, middle, bottom row),
    return a list of 3 sets of words: the words that could cross it in the 0th, 2nd and 4th column.
    Remove the given word from each set
    e.g. If the word is PETER and the position is 0, it will return
    a set of words beginning with P, a set of words beginning with T, and a set of words beginning with R,
    """
    return [
        mapping[(position, word[0])] - set([word]),
        mapping[(position, word[2])] - set([word]),
        mapping[(position, word[4])] - set([word]),
    ]


def check_intersection(word_set_1, word_set_2):
    """ Given two lists of 3 sets, returns the intersection of each pair of sets"""
    return [
        word_set_1[0] & word_set_2[0],
        word_set_1[1] & word_set_2[1],
        word_set_1[2] & word_set_2[2],
    ]


def count_letter_occurrences(grid, word):
    counts = Counter(word + ''.join(grid))
    return max(counts.values())


def make_grid(mapping, all_words, i):
    shuffle(all_words)
    print(i)

    def get_next_word(grid, position=0, down_words=None):
        for word in all_words:
            if word in grid: #or count_letter_occurrences(grid, word) > 4:
                continue
            down_words_2 = get_intersecting_words(mapping, word, position)

            if position > 0:
                intersection = check_intersection(down_words, down_words_2)
            else:
                intersection = down_words_2

            # Check there is at least one word in each set of intersections
            if all(word_set for word_set in intersection):
                new_grid = grid + [word]
                if position < 4:
                    # Check for the next horizontal word
                    result = get_next_word(new_grid, position + 2, intersection)
                    # If we have been sucessful, then we can quit
                    if result:
                        return result
                else:
                    # We have found 3 horizontal words, so find the vertical words that intersection
                    for j in range(3):
                        while True:
                            try:
                                vertical_word = intersection[j].pop()
                            except KeyError:
                                # Run out of words so we fail
                                return False
                            
                            if vertical_word not in new_grid: #and count_letter_occurrences(new_grid, vertical_word) < 5:
                                break
                        new_grid += [vertical_word]
                    
                    # Return answer as a tuple so we can store in a set
                    return tuple(new_grid)

        # No matches so we failed to find a word 
        return False

    return get_next_word([])


def is_good_grid(grid):
    """
    Given a list of 6 words, are all the words different and is there 12 - 16 unique letters
    """
    # Get number of distinct letters
    counts = Counter(''.join(grid))
    num_letters = len(counts.values())
    if max(counts.values()) > 5 and num_letters < 12 or num_letters > 16:
        # print(grid, num_letters, len(set(grid)))
        return False
    return True


def write_grids(filename, grids):
    with open(filename, 'w') as f:
        for grid in grids:
            f.write(', '.join(grid) + '\n')


def append_grid(filename, grid):
    with open(filename, 'a') as f:
        f.write(', '.join(grid) + '\n')


def test_grid_word_counts(filename):
    word_counts = Counter()

    with open(filename, 'r') as f:
        for line in f:
            words = line.strip().split(', ')
            for word in words:
                word_counts[word] += 1
    
    print(word_counts)


def test_grid_letter_occurrences(filename):
    with open(filename, 'r') as f:
        for line in f:
            words = line.strip().replace(', ', '')
            counts = Counter(words)
            print(counts)
            print(max(counts.values()))


if __name__ == '__main__':
    all_words = get_words('wordbank v3b.txt')
    mapping = get_letter_mapping(all_words)

    NUM_GRIDS = 100000
    MAX_WORD_COUNT = NUM_GRIDS * 0.005

    word_counts = Counter()
    grids = set()

    while len(grids) < NUM_GRIDS:
        grid = make_grid(mapping, all_words, len(grids))
        if grid not in grids and is_good_grid(grid):
            grids.add(grid)
            append_grid('letter_grids_1.txt', grid)

            for word in grid:
                word_counts[word] += 1
                if word_counts[word] >= MAX_WORD_COUNT:
                    all_words.remove(word)
                    mapping = get_letter_mapping(all_words)

    # write_grids('letter_grids_1.txt', grids)

    # test_grid_letter_occurrences('letter_grids.txt')
