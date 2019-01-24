import os
from utils import get_word_counts
from collections import defaultdict


def get_most_common_words(word_counts, num=10):
    common_word_counts = []

    for i, (word, count) in enumerate(sorted(word_counts.items(), key=lambda word: -word[1])):
        common_word_counts.append((word, count))
        if (i == num - 1):
            break

    return common_word_counts


def get_length_distribution(word_counts):
    length_distribution = defaultdict(int)

    for word, count in word_counts.items():
        length_distribution[len(word)] += count

    return length_distribution


if __name__ == '__main__':
    import os
    word_counts = get_word_counts(os.path.join('word_lists', 'filtered_word_counts.txt'))

    common_word_counts = get_most_common_words(word_counts)
    length_distribution = get_length_distribution(word_counts)
    print(length_distribution)

