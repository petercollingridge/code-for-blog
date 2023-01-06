from collections import defaultdict
from math import log

from utils import get_words


def get_colours(guess, target):
    """
    Given a guessed word and a target word return a list of 3 lists.
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


def get_colour_string(guess, target):
    """
    Given a guessed word and a target word string representing the colours of the tiles,
    e.g. 'G-YY-'
    """
    tiles = ['-', '-', '-', '-', '-']
    target = list(target)

    for i in range(5):
        if guess[i] == target[i]:
            tiles[i] = 'G'
            target[i] = '_'             # Mark letter as used

    for i in range(5):
        try:
            index = target.index(guess[i])
            tiles[i] = 'Y'
            target[index] = '_'     # Mark letter as used
        except ValueError:
            pass

    return ''.join(tiles)


def test_get_colour_string():
    def test_score(guess, word, expected):
        print(guess, word)
        result = get_colour_string(guess, word)
        assert(result == expected)

    # No matches
    test_score('ABCDE', 'FGHIJ', '-----')
    # One exact match
    test_score('AxCDE', 'FxHIJ', '-G---')
    # One match in the wrong place
    test_score('AxCDE', 'FGxIJ', '-Y---')

    # Two of the same letter in wrong positions
    test_score('xBxDE', 'FxHxJ', 'Y-Y--')
    # Two of the same letter, one in the wrong position
    test_score('xBxDE', 'xGHxJ', 'G-Y--')
    # One letter in the right place, but an extra copy as a guess
    test_score('xxCDE', 'xGHIJ', 'G----')
    # # One letter in the answer, two in the guess, both in the wrong position
    test_score('xxCDE', 'FGxIJ', 'Y----')
    # Guess three of the letter, one right, one wrong position, other missing
    test_score('xBxDx', 'xGHxJ', 'G-Y--')


def get_colours_2(guess, target, colours=None):
    """
    Another get get which tiles should be coloured, that is easy to combine
    with existing colour information.
    Return a list of 3 objects
    First (green) is a dictionary that maps a letter to its index
    Second (yellow) is a dictionary that maps a letter to a list of indices it is not
    Third (grey) is a set of letters which have been ruled out
    """

    if not colours:
        colours = [dict(), defaultdict(list), set()]

    target = list(target)

    for i in range(5):
        letter = guess[i]
        if letter == target[i]:
            colours[0][i] = letter
            target[i] = '_'             # Mark letter as used
        else:
            try:
                index = target.index(letter)
                target[index] = '_'     # Mark letter as used
                colours[1][letter].append(i)
            except ValueError:
                colours[2].add(letter)

    return colours


def convert_colour_string_to_information(word, colours, information=None):
    """ Convert a word and a, string of colours in the form 'G-YYG- into a list of information. """

    if not information:
        information = [dict(), set(), set()]

    for i in range(5):
        if colours[i] == 'G':
            information[0][i] = word[i]
        elif colours[i] == 'Y':
            information[1].add((i, word[i]))
        else:
            information[2].add((i, word[i]))

    return information


def test_convert_colour_string_to_information():
    colours1 = get_colours_2('RAISE', 'CRAZE')
    print(colours1)
    colours2= get_colours_2('BLARE', "CRAZE", colours1)
    print(colours2)


    info1 = convert_colour_string_to_information('RAISE', 'YY--G')
    print(info1)
    info2 = convert_colour_string_to_information('BLARE', '--GYG', info1)
    print(info2)


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


def is_word_consistent_with_colour_string(target, guess, colour_string):
    """
    Test is a target word is consistent with the information from a guess.
    Guess is another word and colour_string is a string representing the colours of the tiles.
    """

    # Copy word into list so we can overwrite letters we have already matched
    target_letters = list(target)

    # Check for matches
    for i in range(5):
        if colour_string[i] =='G':
            if target_letters[i] != guess[i]:
                return False
            else:
                # Mark letter as used
                target_letters[i] = '_'

    # Check for letter is the wrong positions
    for i in range(5):
        if colour_string[i] =='Y':
            if guess[i] == target_letters[i]:
                # Letter is in target, but in the same place
                return False
            try:
                index = target_letters.index(guess[i])
                target_letters[index] = '_'     # Mark letter as used
            except ValueError:
                # Letter not in target
                return False

    # Check for letters that shouldn't be in the target
    for i in range(5):
        if colour_string[i] =='-' and guess[i] in target_letters:
            return False

    return True


def is_word_consistent_with_colour_string_simple(target, guess, colour_string):
    return colour_string == get_colour_string(guess, target)


def get_consistent_words(targets, guess, result):
    return [
        target for target in targets if is_word_consistent_with_colour_string(target, guess, result)
    ]   


def get_possible_words_for_multiple_results(targets, guesses):
    possible_words = targets
    for guess_word, result in guesses:
        possible_words = get_consistent_words(possible_words, guess_word, result)
    return possible_words


def test_is_word_consistent_with_colour_string():
    # Info says no matches and word has no matches
    assert(is_word_consistent_with_colour_string('ABCDE', 'FGHIJ', '-----') == True)
    # Info says no matches and word has a match
    assert(is_word_consistent_with_colour_string('ABCDE', 'AGHIJ', '-----') == False)
    # Info says no matches and word has a match in wrong place
    assert(is_word_consistent_with_colour_string('ABCDE', 'FGHIA', '-----') == False)

    # Info says all letter match but in wrong place
    assert(is_word_consistent_with_colour_string('ABCDE', 'BCDEA', 'YYYYY') == True)

    assert(is_word_consistent_with_colour_string('raise', 'peace', '-Y--Y') == False)
    # Two letters in target, one in guess, in the right place
    assert(is_word_consistent_with_colour_string('peace', 'raise', '-Y--Y') == False)

    # Info says one match and word has no matches
    assert(is_word_consistent_with_colour_string('ABCDE', 'FGHIJ', 'G----') == False)
    # Info says one match and word has a match
    assert(is_word_consistent_with_colour_string('ABCDE', 'AGHIJ', 'G----') == True)
    # Info says one match and word has a match in the wrong place
    assert(is_word_consistent_with_colour_string('ABCDE', 'FGHIA', '----G') == False)

    # Info says one match in wrong place and word has no matches
    assert(is_word_consistent_with_colour_string('ABCDE', 'FAHIJ', 'Y----') == False)
    # Info says one match in wrong place and word has a match
    assert(is_word_consistent_with_colour_string('ABCDE', 'AGHIJ', 'Y----') == False)
    # Info says one match in wrong place and word has a match in the wrong place
    assert(is_word_consistent_with_colour_string('ABCDE', 'FGHIA', '----Y') == True)

    # Info says two matches and is correct
    assert(is_word_consistent_with_colour_string('AxCxE', 'FxHxJ', '-G-G--') == True)
    # Info says one match and one match in wrong place and is correct
    assert(is_word_consistent_with_colour_string('AxCxE', 'FxxIJ', '-GY--') == True)
    # Two letters in the wrong place, and a duplicate in the target
    assert(is_word_consistent_with_colour_string('fewer', 'crate', '-Y--Y') == True)
    # Target has two different letters in the wrong place
    assert(is_word_consistent_with_colour_string('AyCxE', 'FGxIy', '--Y-Y') == True)
    # Target has two letters the same in the wrong place
    assert(is_word_consistent_with_colour_string('AxCxE', 'FGxIx', '--Y-Y') == True)
    # Guess has three letters the same, with two matches
    assert(is_word_consistent_with_colour_string('AxCxE', 'FxxxJ', '-G-G-') == True)
    # Target has three letters the same, with two matches
    assert(is_word_consistent_with_colour_string('AxxxE', 'FxHxJ', '-G-G-') == True)
    # Target has three letters the same, with two matches and one in the wrong place
    assert(is_word_consistent_with_colour_string('AxxxE', 'FxHxx', '-G-GY') == True)

    print('test_is_word_consistent_with_colour_string')


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


def get_score_distribution_for_guess(guess, target_list):
    """
    For all words in a list of target words, get the result when playing a given guess.
    Return a dictionary mapping the colour string to a count of how many targets would give that pattern of colours.
    """

    scores = defaultdict(int)
    for target in target_list:
        score = get_colour_string(guess, target)
        scores[score] += 1
    return scores


def get_all_sets_of_words_for_guess(guess, target_list):
    """
    For all words in a list of target words, get the result when playing a given guess.
    Returns a dictionary mapping a colour score to a list of possible results,
    e.g. for guess = RAISE, { 'G-Y--': ['RHINO', 'ROBIN',]
    """

    scores = defaultdict(list)
    for target in target_list:
        score = get_colour_string(guess, target)
        scores[score].append(target)
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
    scores = get_score_distribution_for_guess(guess, word_list)
    return sum(count * count for count in scores.values()) / n


def get_information_from_word(guess, word_list):
    """ For a given guess, calculate the expected number of remaining words after playing it,
        by considering all possible targets.
    """

    # n = len(word_list)
    scores = get_score_distribution_for_guess(guess, word_list)
    return sum(count * log(count) for count in scores.values()) #/ n


def get_largest_group(guess, word_list):
    scores = get_score_distribution_for_guess(guess, word_list)
    return max(scores.values())


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


def get_least_worse_guess(possible_guesses, possible_answers):
    # Most informative word has the smallest information
    min_largest_group = get_largest_group(possible_guesses[0], possible_answers)
    best_guess = possible_guesses[0]

    for guess in possible_guesses[1:]:
        largest_group = get_largest_group(guess, possible_answers)
        # print(guess, information)
        if largest_group < min_largest_group:
            min_largest_group = largest_group
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
        print(result, best_guess)
        # print(result, best_guess, words)


def count_required_guess(all_words, answer_list, first_guess):
    """
    For a given starting word, calculate the expected number of moves to guess the answer
    for each possible answer, assuming to use the most informative word at each point
    """

    moves = {}

    def test_word_set(guess, possible_answers, count):
        word_sets = get_all_sets_of_words_for_guess(guess, possible_answers)
        
        if 'wound' in possible_answers:
            print(count, guess)

        for colour_string, words in word_sets.items():
            if colour_string == 'GGGGG':
                # We found the answer
                moves[words[0]] = count
            elif len(words) == 1:
                # Only one possible answer remains, so we can get in the next guess
                moves[words[0]] = count + 1
            elif len(words) == 1:
                # Two possible answers remain, so we can get one in the next guess,
                # the other in the next
                moves[words[0]] = count + 1
                moves[words[1]] = count + 2
            else:
                # Find the best word to use for the remaining set of words
                # best_guess = get_most_informative_guess(all_words, words)
                # best_guess = get_least_worse_guess(words, words)
                best_guess = get_most_informative_guess(words, words)
                test_word_set(best_guess, words, count + 1)

    test_word_set(first_guess, answer_list, 1)

    return moves


def find_best_word_for_winning_in_two(all_words, all_answers):
    max_score = 0
    best_word = None

    for word in all_words:
        word_sets = get_all_sets_of_words_for_guess(word, all_answers)
        score = sum(1 for _set in word_sets.values() if len(_set) == 1)
        print(word, score)

        for _set in word_sets.values():
            if len(_set) == 1:
                print(_set)

        if score > max_score:
            max_score = score
            best_word = word

    print(best_word, max_score)


def find_least_failing_word(valid_answers, valid_words):
    min_fails = 3000
    best_words = []

    for i, word in enumerate(valid_words):
        guesses = count_required_guess(valid_answers, valid_answers, word)
        fail_words = sum(1 for turns in guesses.values() if turns > 6)
        print(i, word, fail_words)
        if fail_words < min_fails:
            min_fails = fail_words
            best_words = [word]
        elif fail_words == min_fails:
            best_words.append(word)

    print(min_fails, best_words)


def suggest_guess(valid_answers, current_guesses):
    words = get_possible_words_for_multiple_results(valid_answers, current_guesses)
    return get_most_informative_guess(words, words)


if __name__ == '__main__':
    # test_get_colours()
    # test_get_colour_string()
    # test_convert_colour_string_to_information()
    # test_is_word_consistent_with_information()
    # test_is_word_consistent_with_colour_string()

    valid_answers = get_words('word_list.txt')
    valid_words = get_words('valid_words.txt') + valid_answers

    # _try_bad_words(words)

    # print(get_score_distribution_for_guess('raise', valid_answers))
    # print(get_all_sets_of_words_for_guess('raise', valid_answers))
    # print(get_expected_remaining_options('raise', valid_answers))
    # print(get_information_from_word('raise', valid_answers))

    # find_best_starting_word(valid_words, valid_answers)
    # find_best_starting_word(valid_answers, valid_answers)

    # print(get_most_informative_guess(valid_words, valid_answers))

    # find_best_second_word('slate', valid_answers)

    # option_split = get_all_sets_of_words_for_guess('nymph', valid_answers)
    # for result, words in option_split.items():
    #     print(result, len(words), words)

    guess = suggest_guess(valid_answers, [
        ('least', 'Y-Y--'),
        ('final', '---YY'),
        ('valor', '-GY--'),
        ('badly', '-G-G-'),
        # ('booby', '-G--G'),
    ])
    print(guess)

    # print(is_word_consistent_with_colour_string('boxer', 'rover', '-G-GG'))

    good_words = [
        'raise',
        'slate',
        'crate',
        'irate',
        'trace',
        'arise',
        'stare',
        'snare',
        'arose',
        'least',

        'stand',
        'flick',
        'spend',
        'belch',
        'growl',
        'smelt',
        'nymph',
        'bland',
        'blast',
        'final',
        'bluer',
        'jumbo',
        'chalk',
        'blend',
        'flame',
        'waver',
        'munch',

        'soare',
        'roate',
        'raile',
        'reast',
        'salet',
        'orate',
        'carte',
        'raine',
        'caret',
        'ariel',

    ]

    # guesses = count_required_guess(valid_answers, valid_answers, 'slate')
    # sorted_results = sorted(guesses.keys(), key=lambda word: guesses[word])
    # for word in sorted_results:
    #     print(word, guesses[word])


    # for word in good_words:
    #     guesses = count_required_guess(valid_answers, valid_answers, word)
    #     # guesses = count_required_guess(valid_words, valid_answers, word)
    #     mean_turns = sum(n for n in guesses.values()) / len(guesses.values())
    #     fail_words = sum(1 for turns in guesses.values() if turns > 6)
    #     print(word, mean_turns, fail_words)

    # find_least_failing_word(valid_answers, valid_answers)

    word ='raise'
    guesses = count_required_guess(valid_answers, valid_answers, word)
    mean_turns = sum(n for n in guesses.values()) / len(guesses.values())
    fail_words = [word for word, turns in guesses.items() if turns > 6]
    # print(word, mean_turns, fail_words)

    # find_best_word_for_winning_in_two(valid_words, valid_answers)
    # find_best_word_for_winning_in_two(['laten'], valid_answers)
