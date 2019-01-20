import os
from utils import get_word_counts


def show_most_common_words(word_counts, num=10):
    for i, (word, count) in enumerate(sorted(word_counts.items(), key=lambda word: -word[1])):
        print(word, count)
        if (i == num - 1):
            break


if __name__ == '__main__':
    import os
    word_counts = get_word_counts(os.path.join('word_lists', 'filtered_word_counts.txt'))
    show_most_common_words(word_counts)
    print(word_counts['be'])
