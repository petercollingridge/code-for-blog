from utils import get_word_counts, show_in_order
from collections import defaultdict, Counter


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


def find_words_containing_substring(words, substring):
    return [word for word in words if substring in word]


if __name__ == '__main__':
    import os
    word_counts = get_word_counts(os.path.join('word_lists', 'filtered_word_counts.txt'))
    words = word_counts.keys()
    bigrams = get_bigram_frequencies(word_counts)

    # show_in_order(bigrams)
    # total_bigrams = sum(count for count in bigrams.values())
    # print(total_bigrams)

    # for bigram, count in sorted(bigrams.items(), key=lambda item: item[1])[:10]:
    #     print(bigram, count, find_words_containing_substring(words, bigram))

    # Top 40 bigrams
    top_bigrams = [item for item, count in sorted(bigrams.items(), key=lambda item: item[1])[:40]]
    letter_counts = Counter("".join(top_bigrams))
    print(letter_counts)