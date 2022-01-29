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


if __name__ == '__main__':
    valid_words = get_words('valid_words.txt')
    valid_answers = get_words('word_list.txt')

    print(get_letter_frequencies(valid_answers))
    print(count_letters(valid_answers))

    print(count_distinct_letters(valid_words))
    print(get_repeated_letters('tepee', 2))
    get_repeated_letter_counts(valid_answers, 3)
