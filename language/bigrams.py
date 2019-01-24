from utils import get_word_counts
from collections import defaultdict


def get_bigram_frequencies(word_counts):
    bigrams = defaultdict(int)

    for word, count in word_counts.items():
        first_character = word[0]
        for second_character in word[1:]:
            bigrams[first_character + second_character] += count
            first_character = second_character

    return bigrams


if __name__ == '__main__':
    import os
    word_counts = get_word_counts(os.path.join('word_lists', 'filtered_word_counts.txt'))
    bigrams = get_bigram_frequencies(word_counts)

    print(bigrams)
