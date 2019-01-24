import os
from collections import defaultdict 


def get_word_list(filepath):
    """ Open a file of words separated by new lines and return a list of them. """

    with open(filepath, 'r') as f:
        return [word.strip() for word in f]


def filter_word_list(word_list):
    """ Given a word list return al
    l the words that consist of just letters. """
    return list(filter(lambda word: word.islower() and word.isalpha(), word_list))


def get_word_counts(filepath):
    """ Read a tab-delimited file of words and their counts,
        where the first value is the word count and the second is the word. """
    
    words = defaultdict(int)

    with open(filepath, 'r') as f:
        for line in f:
            temp = line.split("\t")
            if len(temp) > 1:
                words[temp[1]] += int(temp[0])

    return words


def filter_word_counts(word_counts, white_list):
    """ Given a dict of word_counts, combine counts that are the same,
        and remove words that are not in the """

    filtered_counts = {}
    white_list_set = set(white_list)

    for word, count in word_counts.items():
        word = word.lower()
        if word in white_list_set:
            filtered_counts[word] = count

    return filtered_counts


def get_total_count(word_counts, words):
    return sum(word_counts.get(word, 0) for word in words)


def find_most_common_excluded_word(word_counts, set_of_words, max_count=1):
    """
    Given a dict mapping words to their counts and a set of words,
    find the word in the dict that is not in set, with the highest count
    """

    count = 0

    for word in sorted(word_counts, key=lambda word: word_counts[word], reverse=True):
        if word not in set_of_words:
            print(word, word_counts[word])
            count += 1
            if count == max_count:
                break


def write_word_counts(filename, word_counts, limit=0):
    """
    Write to a file a dictionart of word frequencies starting with the most frequent.
    If <limit> is set, then only write the first <limit> words.
    """

    count = 0
    with open(filename, 'w') as f:
        for word, count in sorted(word_counts.items(), key=lambda x: -x[1]):
            f.write("{}\t{}\n".format(word, count))
            count += 1
            if limit and count >= limit:
                break


if __name__ == '__main__':
    # Get word frequencies
    word_counts = get_word_counts(os.path.join('..', 'word_lists', '500k_wordlist.txt'))
    set_of_words = set(word_counts.keys())
    # # print(len(set_of_words))  #365,749
    # # print(get_total_count(word_counts, set_of_words))  #404,253,213

    # Get list of common words from http://www.gutenberg.org/files/3201/files/
    # common_words = get_word_list(os.path.join('..', 'COMMON.TXT'))
    common_words = get_word_list(os.path.join('..', 'word_lists', 'CROSSWD.TXT'))
    # print(len(common_words))    #113,811

    # Find longest words in common_words
    # print(max(len(word) for word in common_words))    # 21
    # print(list(word for word in common_words if len(word) == 21))

    # # Filtering
    filtered_words = set_of_words.intersection(set(common_words))
    # print(len(filtered_words))  # 113,811
    # print(get_total_count(word_counts, filtered_words))  #372,853,319
    # find_most_common_excluded_word(word_counts, filtered_words, 10)

    # Find words missing from COCA 
    # lost_words = set(common_words) - set_of_words
    # print([lost_words.pop() for _ in range(10)])

    # Save list of filtered words and their counts
    filtered_word_counts = {word: word_counts[word] for word in filtered_words}
    write_word_counts(os.path.join('..', 'word_lists', 'filtered_word_counts.txt'), filtered_word_counts)
