import os
import math
from collections import Counter, defaultdict


def get_all_words(filename):
    """ Given a filename to a list of words, return a list of 5-letter words. """

    words = []
    with open(filename, 'r') as f:
        for line in f:
            word = line.strip()
            if len(word) == 5:
                words.append(word)

    return words


def get_words(filename):
    """ Given a filename to a list of words, return a list of 5-letter words. """

    words = []
    with open(filename, 'r') as f:
        for line in f:
            words.append(line.strip())

    return words


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
            count += 1

        for letter in repeated_letters:
            letters[letter] += 1

    print(count)
    print(letters)


def get_letter_frequencies(words):
    """ Given a list of words return a Counter of how often each letter appears in them. """
    count = Counter()
    for word in words:
        count += Counter(word)
    return  count


def count_letters(words):
    """ Get a count for the nth letter of the words in the word list. """

    counters = []
    for i in range(5):
        counters.append(Counter(word[i] for word in words))
    return counters


def get_word_scores(words, counts):
    """
    Score every word in a list of words based on how many other words have a matching
    letter a each position.
    """
    def get_score(word):
        score = 1
        for i in range(5):
            score *= counts[i][word[i]]
        return score

    return { word: get_score(word) for word in words }


def score_guess(guess, target):
    """
    Given a guessed word and a target word return an array of letter information.
    Values are 0: no match, 1: letter in word, 2: letter in place
    """
    score = []
    target = list(target)

    for i in range(5):
        if guess[i] == target[i]:
            score.append(2)
            target[i] = '_'     # Mark letter as used
        else:
            try:
                index = target.index(guess[i])
                target[index] = '_'     # Mark letter as used
                score.append(1)
            except ValueError:
                score.append(0)
    return score


def score_guess_2(guess, target):
    """
    Given a guessed word and a target word return a list of 3 listss.
    The first is a list of letters that match (green);
    The second is a list of letters that partially match (yellow);
    The third is a list of letters that don't match (grey);
    """
    matches = []
    near_misses = []
    misses = []
    target = list(target)

    for i in range(5):
        if guess[i] == target[i]:
            matches.append(i)
            target[i] = '_'             # Mark letter as used
        else:
            try:
                index = target.index(guess[i])
                target[index] = '_'     # Mark letter as used
                near_misses.append(i)
            except ValueError:
                misses.append(i)
    return (tuple(matches), tuple(near_misses), tuple(misses))


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

    # for i in range(5):
        # if state == 0:
        #     # Guessed letter is not in word
        #     # Or is it in word but is accounted for by another guess
        #     # TODO: could be wrong if letter is in an accepted position
        #     return guess_letter not in word

        # if state == 1:
        #     # Guessed letter is in word, but not in this position
        #     # and not accounted for by another guess
        #     return guess_letter != target_letter and guess_letter in word
        
        # if state == 2:
        #     # 2 means letters should match
        #     return guess_letter == target_letter
    # return True


def test_if_word_consistent_with_guesses(word, guesses, results):
    """ Run test_if_word_consistent_with_guess with a array of guesses and results. """

    for guess, result in zip(guesses, results):
        if not is_word_consistent_with_information(word, guess, result):
            return False
    return True


def find_possible_words_for_guess(word_list, guess, result):
    return [word for word in word_list if is_word_consistent_with_information(word, guess, result)]


def find_possible_words_for_guesses(word_list, guesses, result):
    return [word for word in word_list if test_if_word_consistent_with_guesses(word, guesses, result)]


def get_all_scores_for_guess(guess, word_list):
    """ For a given guess, calculate the score for each possible word. """

    scores = defaultdict(int)
    for word in word_list:
        score = score_guess(guess, word)
        scores[tuple(score)] += 1
    return scores


def get_expected_remaining_options(guess, word_list):
    n = len(word_list)
    scores = get_all_scores_for_guess(guess, word_list)

    expected_options = 0
    for score, count in scores.items():
        expected_options += count * len(find_possible_words_for_guesses(word_list, guess, score))

    return expected_options / n


def expected_remaining_options_for_words(guesses, word_list):
    for guess in guesses:
        expected_options = get_expected_remaining_options(guess, word_list)
        print(guess, expected_options)


def find_best_starting_word(word_list):
    scores = {}
    for guess in word_list:
        print(guess)
        scores[guess] = get_expected_remaining_options(guess, word_list)

    best_words = sorted(scores.keys(), key=lambda word: scores[word])
    for word in best_words[:10]:
        print(word, scores[word])


def get_expected_tiles(scores, n):
    green = 0
    yellow = 0
    for score, freqeuncy in scores.items():
        green += score.count(2) * freqeuncy
        yellow += score.count(1) * freqeuncy
    return (green / n, yellow / n)


def get_tiles_for_words(guess_words, word_list):
    n = len(word_list)

    for guess_word in guess_words:
        scores = get_all_scores_for_guess(guess_word, word_list)
        result = get_expected_tiles(scores, n)
        print(guess_word, result)


def test_xyl(word_list):
    result = 0
    for word in word_list:
        if 'y' in word:
            print(word)
            result += 1

    return result


def test_get_repeated_letters():
    print(get_repeated_letters('hello'))
    print(get_repeated_letters('civic'))
    print(get_repeated_letters('hello', 3))
    print(get_repeated_letters('fluff', 3))


def test_scoring():
    # No matches
    assert(score_guess('ABCDE', 'FGHIJ') == [0, 0, 0, 0, 0])
    # One exact match
    assert(score_guess('AxCDE', 'FxHIJ') == [0, 2, 0, 0, 0])
    # One match in the wrong place
    assert(score_guess('AxCDE', 'FGxIJ') == [0, 1, 0, 0, 0])

    # Two of the same letter in wrong positions
    assert(score_guess('xBxDE', 'FxHxJ') == [1, 0, 1, 0, 0])
    # Two of the same letter, one in the wrong position
    assert(score_guess('xBxDE', 'xGHxJ') == [2, 0, 1, 0, 0])
    # One letter in the right place, but an extra copy as a guess
    assert(score_guess('xxCDE', 'xGHIJ') == [2, 0, 0, 0, 0])
    # One letter in the answer, two in the guess, both in the wrong position
    assert(score_guess('xxCDE', 'FGxIJ') == [1, 0, 0, 0, 0])


def test_scoring_2():
    def test_score(guess, word, expected):
        print(guess, word)
        result = score_guess_2(guess, word)
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


if __name__ == '__main__':
    word_list_file = 'word_list.txt'
    # word_list = get_words(word_list_file)

    # test_scoring()
    # test_scoring_2()
    # test_is_word_consistent_with_information()

    # print(get_letter_frequencies(words))
    # get_repeated_letter_counts(words, 3)

    # counts = count_letters(words)

    # print(test_if_word_consistent_with_guess('quiet', 'tires', [1, 1, 0, 2, 0]))




    starting_words = ['soare', 'cares', 'roast', 'tires', 'tares', 'saint', 'tails', 'ninja', 'xylyl', 'affix']

    # sorted_words = sorted(words, key=lambda word: scores[word])
    # print(sorted_words[-1], scores[sorted_words[-1]])
    # print(sorted_words[-10:])

    # result = test_if_word_consistent_with_information('quiet', 'tires', [1, 1, 0, 2, 0])
    # result = test_if_word_consistent_with_information('favor', 'groan', [0, 1, 1, 1, 1])

    # result = test_if_word_consistent_with_guesses('solar', ['tares', 'sharp'], [[0, 1, 1, 0, 1], [2, 0, 1, 1, 0]])
    # print(result)

    # result = find_possible_words_for_guesses(
    #     words,
    #     ['raise', 'thank'],
    #     [[0, 1, 0, 0, 0], [0, 0 ,1 , 0, 1]]
    # )
    # result = find_possible_words_for_guesses(words, ['raise'], [[0, 0, 2, 0, 0]])
    # print(result)

    # print(get_expected_remaining_options('xylyl', words))

    # result = score_guess('sharp', 'solar')
    # print(result)

    # result = get_all_scores_for_guess('raise', words)
    # print(result)
    # print(max(result.values()))
    # print(len(result.values()))

    # result = get_expected_remaining_options('roast', words)
    # print(result)
    # expected_remaining_options_for_words(starting_words, words)
    
    # get_tiles_for_words(['soare', 'cares', 'roast', 'tires', 'tares', 'saint', 'tails'], words)
    # print(test_xyl(words))

    # find_best_starting_word(words)s
