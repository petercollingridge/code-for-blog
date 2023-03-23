from collections import Counter, defaultdict
from time import time
from random import shuffle


def get_words_with_properties(filename):
    words = []
    uncommon_words = set()
    double_letters = set()

    with open(filename, 'r') as f:
        for line in f:
            word, rarity, double = line.strip().split('\t')
            words.append(word)
            if rarity == '1':
                uncommon_words.add(word)
            if double == '1':
                double_letters.add(word)

    return words, uncommon_words, double_letters


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


def get_word_mappings(all_words, letter_mappings, uncommon_words, double_letters):
    """
    Get a dictionary that maps each word in all_words to a 3x3 grid of sets of words that can intersect
    that word at that point,
    
    e.g. expel: [
        [{ words with E at position 1}, { words with P at position 1}, { words with L at position 1}],
        [{ words with E at position 3}, { words with P at position 3}, { words with L at position 3}],
        [{ words with E at position 5}, { words with P at position 5}, { words with L at position 5}],
    ]

    If a word is uncommon then none of its words can be uncommon.
    If a word has a double letter then none of its words can have a double letter.
    """

    word_mapping = {}
    for word in all_words:
        # Word should not intersect with itself
        disallowed_words = { word }

        # An uncommon words can't intersect with another uncommon word
        # if word in uncommon_words:
        #     disallowed_words |= uncommon_words

        # A word with a double letter can't intersect with another
        if word in double_letters:
            disallowed_words |= double_letters

        word_mapping[word] = [
            [
                letter_mappings[(0, word[0])] - disallowed_words,
                letter_mappings[(0, word[2])] - disallowed_words,
                letter_mappings[(0, word[4])] - disallowed_words,
            ],
            [
                letter_mappings[(2, word[0])] - disallowed_words,
                letter_mappings[(2, word[2])] - disallowed_words,
                letter_mappings[(2, word[4])] - disallowed_words,
            ],
            [
                letter_mappings[(4, word[0])] - disallowed_words,
                letter_mappings[(4, word[2])] - disallowed_words,
                letter_mappings[(4, word[4])] - disallowed_words,
            ],
        ]

    return word_mapping


def count_intersecting_words(word_mapping):
    counts = Counter()
    for word, intersection_words in word_mapping.items():
        counts[word] = sum(len(intersection_words[x][y]) for x in range(3) for y in range(3))

    return counts


def count_unique_words(filename):
    grids = read_grids(filename)
    words = set()
    for grid in grids:
        for word in grid:
            words.add(word)
    print(len(words))


def get_intersecting_words(mapping, word, position):
    """
    Given a word and its position (0, 2 or 4 for top, middle, bottom row),
    return a list of 3 sets of words: the words that could cross it in the 0th, 2nd and 4th column.
    Remove the given word from each set
    e.g. If the word is PETER and the position is 0, it will return
    a set of words beginning with P, a set of words beginning with T, and a set of words beginning with R,
    """
    this_word = set([word])
    return [
        mapping[(position, word[0])] - this_word,
        mapping[(position, word[2])] - this_word,
        mapping[(position, word[4])] - this_word,
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
            if word in grid: # or count_letter_occurrences(grid, word) > 4:
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
                    # We have found 3 horizontal words, so find the vertical words that intersect
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


def make_grid2(mapping, all_words, over_used_words):
    shuffle(all_words)

    def get_next_word(grid, row=0, down_words=None):
        for word in all_words:
            if word in grid or word in over_used_words:
                continue
            down_words_2 = mapping[word][row]

            if row > 0:
                intersection = check_intersection(down_words, down_words_2)
            else:
                intersection = down_words_2

            # Check there is at least one word in each set of intersections
            if all(word_set for word_set in intersection):
                new_grid = grid + [word]
                if row == 2:
                    # We have found 3 horizontal words, so find the vertical words that intersect
                    for j in range(3):
                        while True:
                            try:
                                vertical_word = intersection[j].pop()
                            except KeyError:
                                # Run out of words so we fail
                                return False
                            
                            if vertical_word not in new_grid and \
                                vertical_word not in over_used_words:
                                break
                        new_grid += [vertical_word]
                    
                    # Return answer as a tuple so we can store in a set
                    return tuple(new_grid)
                else:
                    # Check for the next horizontal word
                    result = get_next_word(new_grid, row + 1, intersection)
                    # If we have been sucessful, then we can quit
                    if result:
                        return result

        # No matches so we failed to find a word 
        return False

    return get_next_word([])


def is_good_grid(grid, uncommon_words, double_letters):
    """
    Given a list of 6 words, are all the words different and is there 12 - 16 unique letters
    """
    # Get number of distinct letters
    counts = Counter(''.join(grid))
    num_letters = len(counts.values())

    if max(counts.values()) > 5:
        return False

    if num_letters < 10 or num_letters > 16:
        # print(grid, num_letters, len(set(grid)))
        return False

    # There must be at least 5 unique starting letters in the grid.
    if len(set(word[0] for word in grid)) < 5:
        return False

    # No two words can have the same starting two letters
    starting_pairs = set(word[:2] for word in grid)
    if len(starting_pairs) < 6:
        return False

    # No more than two uncommon words
    if sum(1 for word in grid if word in uncommon_words) > 2:
        return False

    # No more than two words with a double letter
    if sum(1 for word in grid if word in double_letters) > 1:
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


def get_grids(mapping, all_words, num_grids):
    MAX_WORD_COUNT = num_grids * 0.025

    word_counts = Counter()
    grids = set()
    over_used_words = set()

    start = time()

    with open('letter_grids_fast3.txt', 'a') as f:
        while len(grids) < num_grids:
            grid = make_grid2(mapping, all_words, over_used_words)
            if grid not in grids and is_good_grid(grid, uncommon_words, double_letters):
                print(len(grids))
                grids.add(grid)
                # Write to file as we go in case we want to stop in the middle of runnign
                # append_grid('letter_grids_fast2.txt', grid)
                f.write(', '.join(grid) + '\n')

                for word in grid:
                    word_counts[word] += 1
                    if word_counts[word] >= MAX_WORD_COUNT:
                        pass
                        over_used_words.add(word)

    print(time() - start)

    return grids


def read_grids(filename):
    grids = []

    with open(filename, 'r') as f:
        for line in f:
            grid = tuple(line.strip().split(', '))
            grids.append(grid)

    return grids


def prepare_grids():
    grids = read_grids('new_grids.txt')

    unique_grids = set()
    for grid in grids:
        swapped_grid = (grid[3], grid[4], grid[5], grid[0], grid[1], grid[2])
        if swapped_grid not in unique_grids:
            unique_grids.add(grid)

    print(len(unique_grids))
    write_grids('unique_grids.txt', grids)


def order_grids(filename, filename2):
    MAX_FREQ = 110
    GRID_LENGTH = 50000

    grids = read_grids(filename)
    # How many times since a word last appeared in the final list
    last_appeared = defaultdict(int)

    ordered_grids = []
    index = 0

    while len(ordered_grids) < GRID_LENGTH:
        grid = grids[index]

        # Check that every word in the grid appear at least MAX_FREQ grids ago
        if last_appeared.get(grid[0], MAX_FREQ) >= MAX_FREQ and \
            last_appeared.get(grid[1], MAX_FREQ) >= MAX_FREQ and \
            last_appeared.get(grid[2], MAX_FREQ) >= MAX_FREQ and \
            last_appeared.get(grid[3], MAX_FREQ) >= MAX_FREQ and \
            last_appeared.get(grid[4], MAX_FREQ) >= MAX_FREQ and \
            last_appeared.get(grid[5], MAX_FREQ) >= MAX_FREQ:

            # Add word
            ordered_grids.append(grid)
            print(len(ordered_grids))

            # Remove grid from list
            grids.pop(index)

            # Record that words appear in the latest grid
            for word in grid:
                last_appeared[word] = 0

            for word in last_appeared:
                # Increment time since word appeared
                last_appeared[word] += 1
        else:
            # Try the next word in the grid
            index += 1

        if index >= len(grids):
            index = 0

    write_grids(filename2, ordered_grids)


if __name__ == '__main__':
    # all_words = get_words('wordbank v3b.txt')
    all_words, uncommon_words, double_letters = get_words_with_properties('wordbank v4.txt')

    letter_mapping = get_letter_mapping(all_words)
    word_mapping = get_word_mappings(all_words, letter_mapping, uncommon_words, double_letters)

    # is_good_grid(('attic', 'fable', 'largo', 'awful', 'tuber', 'credo'), uncommon_words, double_letters)

    order_grids('letter_grids_fast3.txt', 'ordered_50.txt')
    # count_unique_words('letter_grids_fast2.txt')

    # counts = count_intersecting_words(word_mapping)
    # print(counts.most_common()[-10:])

    # grids = get_grids(word_mapping, all_words, 100000)

    # write_grids('letter_grids_1.txt', grids)

    # test_grid_letter_occurrences('letter_grids.txt')


 