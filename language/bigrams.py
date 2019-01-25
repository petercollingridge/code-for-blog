from utils import get_word_counts, show_in_order
from collections import defaultdict


def get_bigram_frequencies(word_counts):
    bigrams = defaultdict(int)

    for word, count in word_counts.items():
        first_character = word[0]
        for second_character in word[1:]:
            bigrams[first_character + second_character] += count
            first_character = second_character

    return bigrams


def find_word_containing_substring(words, substring):
    for word in words:
        if substring in "^{}$".format(word):
            return word


if __name__ == '__main__':
    import os
    word_counts = get_word_counts(os.path.join('word_lists', 'filtered_word_counts.txt'))
    bigrams = get_bigram_frequencies(word_counts)

    show_in_order(bigrams)

    print(find_word_containing_substring(word_counts.keys(), 'jn'))