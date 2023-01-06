import string
from collections import Counter, defaultdict
from utils import get_words


def get_letter_frequencies(words):
    """ Given a list of words return a Counter of how often each letter appears in them. """
    count = Counter()
    for word in words:
        count += Counter(word)
    return count


def count_letters(words):
    """ Get a count for the nth letter of the words in the word list. """

    counters = []
    for i in range(5):
        counters.append(Counter(word[i] for word in words))
    return counters


def get_repeated_letters(word, n=2):
    """ Given a word return a list of letters that are repeated n or more times. """
    
    counter = Counter(word)
    return [word for word, count in counter.items() if count >= n]


def get_repeated_letter_counts(words, n=2):
    """ For each word in a given list, count how many words have a repeated letter. """
    count = 0
    letters = Counter()

    for word in words:
        repeated_letters = get_repeated_letters(word, n)
        if repeated_letters:
            print(word)
            count += 1

        for letter in repeated_letters:
            letters[letter] += 1

    print(count)
    print(letters)


def count_distinct_letters(words):
    counts = defaultdict(int)
    for word in words:
        n = len(set(word))
        counts[n] += 1
        if n == 2:
            print(word)
    return counts


def get_word_positions(words):
    frequencies = count_letters(words)

    scores = {}
    for word in words:
        score = 1
        for i in range(5):
            score *= frequencies[i].get(word[i], 0)
        scores[word] = score

    sorted_words = sorted(scores.keys(), key=lambda word: -scores[word])
    for word in sorted_words[:10]:
        print(word, scores[word])


def is_there_a_word_starting_with(words, letters):
    letters = ''.join(letters)

    for word in words:
        if word.startswith(letters):
            # print(word, letters)s
            return True
    return False


def find_valid_words(word_list, word1, word2):
    for word in word_list:
        if word[0] == word2[1] and \
            is_there_a_word_starting_with(word_list, [word1[1], word[1]]) and \
            is_there_a_word_starting_with(word_list, [word1[2], word[1]]) and \
            is_there_a_word_starting_with(word_list, [word1[3], word[1]]) and \
            is_there_a_word_starting_with(word_list, [word1[4], word[1]]):
            print(word)


def get_dicts_for_letters_to_words_in_position(words):
    """
    Get 5 dicts, where the nth dict maps a letter to
    the set of words that have that letter at position n.
    """

    letters = string.ascii_lowercase

    words_with_letters_at_position_i = []
    for i in range(5):
        # dictionary mapping a letter to the set of words with letters at the ith position
        d = {}
        for letter in letters:
            d[letter] = set(word for word in words if word[i] == letter)
        words_with_letters_at_position_i.append(d)

    return words_with_letters_at_position_i


def find_intersecting_sets(word_list):
    """
    Return a dict that maps a word to a list of 15 sets of words.
    The list corresponds to the set of words that intersect with this word when it is a position i,
    and the word is a position j
    """

    words_with_letters_at_position_i = get_dicts_for_letters_to_words_in_position(word_list)

    intersections = {}

    for word in word_list:
        d = {} 
        sizes = []

        for i in range(5):
            # Interested in position i
            words_at_position = words_with_letters_at_position_i[i]
            for j in range(5):
                # Find which words have the same letter at position j as this word has in position i
                word_set = words_at_position[word[j]] - set([word])
                d[(i, j)] = word_set
                if i == 0:
                    sizes.append(len(word_set))

        # Find best starting word by finding which has the largest smallest set for position 1
        d['score'] = min(sizes)

        intersections[word] = d
    
    return intersections


def find_word_grid(intersections, start_word):
    starting_sets = [intersections[start_word][(0, i)] for i in range(5)]
    
    all_target_positions = [
        [(1, i) for i in range(5)],
        [(2, i) for i in range(5)],
        [(3, i) for i in range(5)],
        [(4, i) for i in range(5)],
    ]

    words = set(intersections.keys()) - set([start_word])

    scores = {}
    # Check whether words have consistent word sets
    for target_positions in all_target_positions:
        print(target_positions)
        for word in words:
            word_sets = intersections[word]
            sizes = []
            for i, position in enumerate(target_positions):
                set_size = len(word_sets[position] & starting_sets[i])
                if set_size == 0:
                    break
                else:
                    sizes.append(set_size)
            else:
                print(word)
                starting_sets = [word_sets[position] & starting_sets[i] for i, position in enumerate(target_positions)]
                # print(starting_sets)
                break


if __name__ == '__main__':
    stuart_words = get_words('wordbank.txt')
    valid_answers = get_words('word_list.txt')
    valid_words = get_words('valid_words.txt') + valid_answers

    # print(get_letter_frequencies(valid_answers))
    # print(count_letters(valid_answers))

    # print(count_distinct_letters(valid_words))
    # print(get_repeated_letters('tepee', 2))
    # get_repeated_letter_counts(valid_answers, 3)

    # get_word_positions(valid_answers)

    # find_valid_words(valid_answers, 'saint', 'slate')

    # d = get_dicts_for_letters_to_words_in_position(valid_answers)

    intersections = find_intersecting_sets(stuart_words)
    # for position, words in intersections['equal'].items():
    #     print(position, words)

    # sorted_words = sorted(intersections.keys(), key=lambda word: -intersections[word]['score'])
    # for word in sorted_words[:10]:
    #     print(word)

    # start with CASTS, FACTS, DAMPS
    # find_word_grid(intersections, 'facts')

    get_repeated_letter_counts(stuart_words, 3)

