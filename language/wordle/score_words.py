from collections import defaultdict
from math import log

from utils import get_words


def get_colours(guess, target):
    """
    Given a guessed word and a target word return a list of 3 listss.
    The first is a list of letters that match (green);
    The second is a list of letters that partially match (yellow);
    The third is a list of letters that don't match (grey);
    """
    green = []
    yellow = []
    grey = []
    target = list(target)

    for i in range(5):
        if guess[i] == target[i]:
            green.append(i)
            target[i] = '_'             # Mark letter as used
        else:
            try:
                index = target.index(guess[i])
                target[index] = '_'     # Mark letter as used
                yellow.append(i)
            except ValueError:
                grey.append(i)
    return (tuple(green), tuple(yellow), tuple(grey))


def test_get_colours():
    def test_score(guess, word, expected):
        print(guess, word)
        result = get_colours(guess, word)
        for i in range(3):
            # print(result[i], expected[i])
            assert(result[i] == tuple(expected[i]))

    # No matches
    test_score('ABCDE', 'FGHIJ', [[], [], [0,1,2,3,4]])
    # One exact match
    test_score('AxCDE', 'FxHIJ', [[1], [], [0,2,3,4]])
    # One match in the wrong place
    test_score('AxCDE', 'FGxIJ', [[], [1], [0,2,3,4]])

    # Two of the same letter in wrong positions
    test_score('xBxDE', 'FxHxJ', [[], [0, 2], [1,3,4]])
    # Two of the same letter, one in the wrong position
    test_score('xBxDE', 'xGHxJ', [[0], [2], [1,3,4]])
    # One letter in the right place, but an extra copy as a guess
    test_score('xxCDE', 'xGHIJ', [[0], [], [1,2,3,4]])
    # # One letter in the answer, two in the guess, both in the wrong position
    test_score('xxCDE', 'FGxIJ', [[], [0], [1,2,3,4]])
    # Guess three of the letter, one right, one wrong position, other missing
    test_score('xBxDx', 'xGHxJ', [[0], [2], [1,3,4]])


def is_word_consistent_with_information(target, guess, result):
    """
    Test is a target word is consistent with the information from a guess.
    Guess is another word and result is an array of 0, 1, or 2,
    Where 0 means letter not in word, 1 means letter is in word,
    and 2 means it is in the word in that position.
    """

    # Copy word into list so we can overwrite letters we have already matched
    target_letters = list(target)

    # Check for matches
    for i in result[0]:
        if target_letters[i] != guess[i]:
            return False
        else:
            target_letters[i] = '_'         # Mark letter as used

    # Check for letter is the wrong positions
    for i in result[1]:
        try:
            index = target_letters.index(guess[i])
            if index == i:
                # Letter is in target, but in the same place
                return False
            target_letters[index] = '_'     # Mark letter as used
        except ValueError:
            # Letter not in target
            return False

    # Check for letters that shouldn't be in the target
    for i in result[2]:
        if guess[i] in target_letters:
            return False

    return True


def get_consistent_words(targets, guess, result):
    return [
        target for target in targets if is_word_consistent_with_information(target, guess, result)
    ]   


def test_is_word_consistent_with_information():
    # Info says no matches and word has no matches
    assert(is_word_consistent_with_information('ABCDE', 'FGHIJ', [[], [], [0,1,2,3,4]]) == True)
    # Info says no matches and word has a match
    assert(is_word_consistent_with_information('ABCDE', 'AGHIJ', [[], [], [0,1,2,3,4]]) == False)
    # Info says no matches and word has a match in wrong place
    assert(is_word_consistent_with_information('ABCDE', 'FGHIA', [[], [], [0,1,2,3,4]]) == False)

    # Info says one match and word has no matches
    assert(is_word_consistent_with_information('ABCDE', 'FGHIJ', [[0], [], [1,2,3,4]]) == False)
    # Info says one match and word has a match
    assert(is_word_consistent_with_information('ABCDE', 'AGHIJ', [[0], [], [1,2,3,4]]) == True)
    # Info says one match and word has a match in the wrong place
    assert(is_word_consistent_with_information('ABCDE', 'FGHIA', [[4], [], [0,1,2,3]]) == False)

    # Info says one match in wrong place and word has no matches
    assert(is_word_consistent_with_information('ABCDE', 'FAHIJ', [[], [0], [1,2,3,4]]) == False)
    # Info says one match in wrong place and word has a match
    assert(is_word_consistent_with_information('ABCDE', 'AGHIJ', [[], [0], [1,2,3,4]]) == False)
    # Info says one match in wrong place and word has a match in the wrong place
    assert(is_word_consistent_with_information('ABCDE', 'FGHIA', [[], [4], [0,1,2,3]]) == True)

    # Info says two matches and is correct
    assert(is_word_consistent_with_information('AxCxE', 'FxHxJ', [[1,3], [], [0,2,4]]) == True)
    # Info says one match and one match in wrong place and is correct
    assert(is_word_consistent_with_information('AxCxE', 'FxxIJ', [[1], [2], [0,3,4]]) == True)
    # Target has two different letters in the wrong place
    assert(is_word_consistent_with_information('AyCxE', 'FGxIy', [[], [2, 4], [0,3]]) == True)
    # Target has two letters the same in the wrong place
    assert(is_word_consistent_with_information('AxCxE', 'FGxIx', [[], [2, 4], [0,3]]) == True)
    # Guess has three letters the same, with two matches
    assert(is_word_consistent_with_information('AxCxE', 'FxxxJ', [[1,3], [], [0,2,4]]) == True)
    # Target has three letters the same, with two matches
    assert(is_word_consistent_with_information('AxxxE', 'FxHxJ', [[1,3], [], [0,2,4]]) == True)
    # Target has three letters the same, with two matches and one in the wrong place
    assert(is_word_consistent_with_information('AxxxE', 'FxHxx', [[1,3], [4], [0,2]]) == True)

    print('test_is_word_consistent_with_information')


def get_all_sets_of_colours_for_guess(guess, target_list):
    """ For all words in a list of target words, get the result when playing a given guess. """

    scores = defaultdict(int)
    for target in target_list:
        score = get_colours(guess, target)
        scores[tuple(score)] += 1
    return scores


def get_all_sets_of_words_for_guess(guess, target_list):
    """ For all words in a list of target words, get the result when playing a given guess. """

    scores = defaultdict(list)
    for target in target_list:
        score = get_colours(guess, target)
        scores[tuple(score)].append(target)
    return scores


def convert_score_to_colour(score):
    """ Convert scores in to an easy-to-read format. """
    colours = list('-----')

    for green_index in score[0]:
        colours[green_index] = 'G'
    for yellow_index in score[1]:
        colours[yellow_index] = 'Y'

    return ''.join(colours)


def get_expected_remaining_options(guess, word_list):
    """ For a given guess, calculate the expected number of remaining words after playing it,
        by considering all possible targets.
    """

    n = len(word_list)
    scores = get_all_sets_of_colours_for_guess(guess, word_list)
    return sum(count * count for count in scores.values()) / n


def get_information_from_word(guess, word_list):
    """ For a given guess, calculate the expected number of remaining words after playing it,
        by considering all possible targets.
    """

    # n = len(word_list)
    scores = get_all_sets_of_colours_for_guess(guess, word_list)
    return sum(count * log(count) for count in scores.values()) #/ n


def get_most_informative_guess(possible_guesses, possible_answers):
    # Most informative word has the smallest information
    min_information = get_information_from_word(possible_guesses[0], possible_answers)
    best_guess = possible_guesses[0]

    for guess in possible_guesses[1:]:
        information = get_information_from_word(guess, possible_answers)
        # print(guess, information)
        if information < min_information:
            min_information = information
            best_guess = guess

    return best_guess


def expected_remaining_options_for_words(guesses, word_list):
    for guess in guesses:
        expected_options = get_expected_remaining_options(guess, word_list)
        information = get_information_from_word(guess, word_list)
        print(guess, expected_options, information)


def find_best_starting_word(word_list, target_list=None):
    if not target_list:
        target_list = word_list
    
    scores = {}
    for i, guess in enumerate(word_list):
        print(i, guess)
        scores[guess] = get_information_from_word(guess, target_list)

    sorted_words = sorted(scores.keys(), key=lambda word: scores[word])
    for word in sorted_words[:10]:
        print(word, scores[word])

    print('')

    for word in sorted_words[-10:]:
        print(word, scores[word])


def find_best_second_word(first_word, word_list):
    # Sets of possibilities after one guess
    word_sets = get_all_sets_of_words_for_guess(first_word, word_list)

    sorted_results = sorted(word_sets.keys(), key=lambda word: -len(word_sets[word]))

    for result in sorted_results:
        words = word_sets[result]
        best_guess = get_most_informative_guess(words, words)
        nice_result = convert_score_to_colour(result)
        if nice_result == '-G-GG':
            print(nice_result, best_guess, words)


if __name__ == '__main__':
    # test_get_colours()
    # test_is_word_consistent_with_information()

    valid_answers = get_words('word_list.txt')
    valid_words = get_words('valid_words.txt') + valid_answers

    # _try_bad_words(words)

    # print(get_all_sets_of_colours_for_guess('raise', valid_words))
    # print(get_expected_remaining_options('raise', valid_answers))
    # print(get_information_from_word('raise', valid_answers))

    # find_best_starting_word(valid_words, valid_answers)
    # find_best_starting_word(valid_answers, valid_answers)

    # print(get_most_informative_guess(valid_words, valid_answers))

    find_best_second_word('raise', valid_answers)

    # option_split = get_all_sets_of_words_for_guess('raise', valid_answers)
    # for result, words in option_split.items():
    #     print(convert_score_to_colour(result), len(words))

    words1 = get_consistent_words(valid_answers, 'glint', [[2], [3], (0,1,4)])
    print(words1)
    # words2 = get_consistent_words(words1, 'raises', [(), (4,), (0,1,2,3)])
    # # words3 = get_consistent_words(words2, 'belch', [(), (1,2), (0,3,4)])
    # print(get_most_informative_guess(words2, words2))