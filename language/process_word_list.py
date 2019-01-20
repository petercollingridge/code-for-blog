import os
import string


def get_words(filename):
    words = []
    with open(filename) as f:
        for line in f:
            words.append(line.strip())

    return words


def only_lowercase_letters(word):
    return all((letter in string.ascii_lowercase) for letter in word)


def save_word_list(words, filename):
    with open(filename, 'w') as f:
        f.write('\n'.join(words))


if __name__ == '__main__':
    words = get_words(os.path.join('word_lists', 'COMMON.TXT'))
    words = filter(only_lowercase_letters, words)
    save_word_list(words, os.path.join('word_lists', 'common_filtered.txt'))