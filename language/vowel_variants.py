import os
import subprocess
from string import ascii_lowercase

from process_word_lists.process_word_list import get_word_list
from utils import get_word_counts

VOWELS = 'aeiou'


def get_words_from_unix_dict():
    """ Get list of lowercase words with no hyphens from /usr/share/dict/words. """

    process = subprocess.Popen("cat /usr/share/dict/words".split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode("utf-8")

    words = set(word.lower() for word in output.splitlines() if "-" not in word)
    return words


def get_vowel_variants(words):
    variants = []

    for word in words:
        index = word.find('a')

        if index > -1:
            # Replace the first a with each vowel
            if all(word[:index] + vowel + word[index + 1:] in words for vowel in 'eiou'):
                variants.append(word)

    return variants


def print_longest_variants(variants):
    max_length = max(len(word) for word in variants)
    print(max_length)
    print([word for word in variants if len(word) == max_length])


def get_all_variants(words):
    variants = dict()

    for word in words:
        word_list = []

        for index, letter in enumerate(word):
            for new_letter in ascii_lowercase:
                if new_letter != letter:
                    new_word = word[:index] + new_letter + word[index + 1:]
                    if new_word in words:
                        word_list.append(new_word)

        variants[word] = word_list

    return variants


def print_most_variants(variants, max_count=-1):
    for index, item in enumerate(sorted(variants.items(), key=lambda item: -len(item[1]))):
        print("{} ({}): {}".format(item[0], len(item[1]), ', '.join(item[1])))
        if index == max_count:
            break


if __name__ == '__main__':
    # Get words
    # words = get_words_from_unix_dict()
    # words = set(get_word_list(os.path.join('word_lists', 'CROSSWD.TXT')))
    # words = set(get_word_list(os.path.join('word_lists', 'COMMON.TXT')))
    word_counts = get_word_counts(os.path.join('word_lists', 'filtered_word_counts.txt'))
    words = set(word_counts.keys())

    print(len(words))

    # Get vowel variants
    # variants = get_vowel_variants(words)
    # print(variants)
    # print(len(variants))
    # print_longest_variants(variants)

    # Get all variants
    variants = get_all_variants(words)
    print_most_variants(variants, 10)
    
    