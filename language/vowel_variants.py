import os
import subprocess
from process_word_lists.process_word_list import get_word_list

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


if __name__ == '__main__':
    # words = get_words_from_unix_dict()
    # words = set(get_word_list(os.path.join('word_lists', 'CROSSWD.TXT')))
    words = set(get_word_list(os.path.join('word_lists', 'COMMON.TXT')))
    print(len(words))

    variants = get_vowel_variants(words)
    print(variants)
    print(len(variants))
    
    max_length = max(len(word) for word in variants)
    print(max_length)

    print([word for word in variants if len(word) == max_length])