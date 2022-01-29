# Various experiments
from collections import defaultdict


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


# def is_word_consistent_with_information(target, guess, result):
    # for i in range(5):
    #     if state == 0:
    #         # Guessed letter is not in word
    #         # Or is it in word but is accounted for by another guess
    #         # TODO: could be wrong if letter is in an accepted position
    #         return guess_letter not in word

    #     if state == 1:
    #         # Guessed letter is in word, but not in this position
    #         # and not accounted for by another guess
    #         return guess_letter != target_letter and guess_letter in word
        
    #     if state == 2:
    #         # 2 means letters should match
    #         return guess_letter == target_letter
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


if __name__ == '__main__':
    word_list_file = 'word_list.txt'
    # word_list = get_words(word_list_file)

    # test_scoring()
    # test_scoring_2()
    # test_is_word_consistent_with_information()

    # print(get_letter_frequencies(words))
    # get_repeated_letter_counts(words, 3)

    # counts = count_letters(words)





    starting_words = ['soare', 'cares', 'roast', 'tires', 'tares', 'saint', 'tails', 'ninja', 'xylyl', 'affix']

    # sorted_words = sorted(words, key=lambda word: scores[word])
    # print(sorted_words[-1], scores[sorted_words[-1]])
    # print(sorted_words[-10:])

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
