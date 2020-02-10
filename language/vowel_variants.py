import os
import subprocess
import operator
from math import log, sqrt
from collections import defaultdict, Counter
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


def get_letter_counts(words):
    letter_counts = Counter()
    for word in words:
        letter_counts.update(word)
    return letter_counts


def print_longest_variants(variants, offset=0):
    max_length = max(len(word) for word in variants)
    print(max_length)
    print([word for word in variants if len(word) == max_length - offset])


def print_variant_counts(word, word_counts):
    index = word.find('a')
    if index > -1:
        for vowel in VOWELS:
            word = word[:index] + vowel + word[index + 1:]
            print("{}: {}".format(word, word_counts.get(word, 0)))


def get_letter_swaps(words):
    """
    Given a list of words, return a dict that maps pairs of letters to a 
    list of word pairs, where those two letters are swapped.
    """

    letter_swaps = defaultdict(list)

    for word in words:
        for index, letter in enumerate(word):
            for new_letter in ascii_lowercase[ascii_lowercase.index(letter) + 1:]:
                new_word = word[:index] + new_letter + word[index + 1:]
                if new_word in words:
                    letter_swaps[letter + new_letter].append((word, new_word))

    return letter_swaps


def get_letter_to_letter_swaps(words):
    """
    Given a list of words, return a dict that maps pairs of letters to a 
    list of word pairs, where those two letters are swapped.
    """

    letter_swaps = { letter: defaultdict(list) for letter in ascii_lowercase }

    for word in words:
        for index, letter in enumerate(word):
            for new_letter in ascii_lowercase[ascii_lowercase.index(letter) + 1:]:
                new_word = word[:index] + new_letter + word[index + 1:]
                if new_word in words:
                    letter_swaps[letter][new_letter].append((word, new_word))
                    letter_swaps[new_letter][letter].append((word, new_word))

    return letter_swaps


def get_letter_to_letter_percentages(letter_swaps):
    letter_swap_percentages = dict()

    for letter, swap_letters in letter_swaps.items():
        total = sum(len(words) for words in swap_letters.values())
        letter_swap_percentages[letter] = { swap_letter: len(words) / total for swap_letter, words in swap_letters.items() }

    return letter_swap_percentages

    
def get_letter_swap_proportions(letter_swaps):
    letter_swap_proportions = dict()

    for letter, swaps in letter_swaps.items():
        counts = { 'total': 0 }

        for swap_letter, words in swaps.items():
            counts['total'] += len(words)
            counts[swap_letter] = len(words)

        letter_swap_proportions[letter] = counts

    return letter_swap_proportions


def print_most_swapped_letters(letter_swaps):
    for letter, count in sorted(letter_swaps.items(), key=lambda item: -item[1]['total']):
        print(letter, count['total'])


def print_most_common_letter_each_letter_is_swapped_with(letter_swaps):
    for letter in ascii_lowercase:
        max_count_letter = max(letter_swaps[letter].items(), key=lambda item: len(item[1]))
        print(letter, max_count_letter[0], len(max_count_letter[1]))


def print_proportion_of_words_with_swaps(letter_swaps, letter_counts):
    proportion_of_swapped_letter = { letter: counts['total'] / letter_counts[letter] for letter, counts in letter_swaps.items() } 
    print_most_swapped_letters(proportion_of_swapped_letter)


def print_most_common_letter_to_swap_with_letter(letter_swaps, letter_counts):
    for letter, swaps in sorted(letter_swaps.items(), key=lambda item: item[0]):
        # Sort swaps by amount
        items = (item for item in swaps.items() if item[0] != 'total')

        # Normalised by frequency of letters
        items = ((item[0], item[1] / letter_counts[letter]) for item in items)

        sorted_swaps = sorted(items, key=lambda item: -item[1])
        print(letter, sorted_swaps[0])


def get_all_variants_at_each_postion(words):
    variants = dict()

    for word in words:
        best_word_list = []

        for index, letter in enumerate(word):
            word_list = []

            for new_letter in ascii_lowercase[ascii_lowercase.index(letter) + 1:]:
                new_word = word[:index] + new_letter + word[index + 1:]
                if new_word in words:
                    word_list.append(new_word)

            if len(word_list) > len(best_word_list):
                best_word_list = word_list

        if best_word_list:
            variants[word] = best_word_list

    return variants


def get_words_with_variants_at_each_position(words):
    variants = dict()

    for word in words:
        all_word_lists = []

        for index, letter in enumerate(word):
            word_list = []

            for new_letter in ascii_lowercase:
                if new_letter != letter:
                    new_word = word[:index] + new_letter + word[index + 1:]
                    if new_word in words:
                        word_list.append(new_word)

            if word_list:
                all_word_lists.append(word_list)
            else:
                break

        if len(all_word_lists) == len(word):
            variants[word] = all_word_lists

    return variants


def print_longest_word_with_variants_at_all_positions(variants, word_counts):
    max_length = max(len(word) for word in variants.keys())
    word_scores = []

    for word, word_lists in variants.items():
        if len(word) == max_length:
            # Sort variants
            word_list = [sorted(word_list, key=lambda word: -word_counts[word])[0] for word_list in word_lists]
            score = sum(word_counts[word] for word in word_list)
            word_list_str = "".join(f"<td>{ word }</td>" for word in word_list)

            word_scores.append((word, score))

            # Print table
            # print("<tr>")
            # print(f"  <td>{ word }</td>")
            # print(word_list_str)
            # print("</tr>")
            
    for word in sorted(word_scores, key=lambda score: -score[1]):
        print(word)


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


def get_variants_for_letter(words, target_letter):
    variants = dict()

    for word in words:
        if target_letter not in word:
            continue
        
        word_list = []

        for index, letter in enumerate(word):
            if letter == target_letter:
                for new_letter in ascii_lowercase:
                    if new_letter != letter:
                        new_word = word[:index] + new_letter + word[index + 1:]
                        if new_word in words:
                            word_list.append(new_word)

        variants[word] = word_list

    return variants


def get_distribution_of_variant_numbers(variants):
    return Counter(len(variant_list) for variant_list in variants.values())


def find_longest_word_without_variants(word_counts, variants):
    for word in sorted(word_counts.keys(), key=lambda word: -len(word)):
        if not variants.get(word):
            print(word)
            break


def find_most_common_word_without_variants(word_counts, variants):
    for word, count in sorted(word_counts.items(), key=lambda item: -item[1]):
        if not variants.get(word):
            print(word, count)
            break
 

def print_most_variants(variants, max_count=-1):
    for index, item in enumerate(sorted(variants.items(), key=lambda item: -len(item[1]))):
        # print('<tr>')
        # print('  <td style="border-right: 1px solid #aaa">{}</td>'.format(item[0]))
        # print('  <td>{}</td>'.format(', '.join(item[1])))
        # print('  <td>{}</td>'.format(len(item[1])))
        # print('</tr>')
        print("{} ({}): {}".format(item[0], len(item[1]), ', '.join(word[0] for word in item[1])))
        if index == max_count:
            break


def print_most_variants_for_word_length(variants, word_counts):
    for word_length in range(1, 21):
        filtered_variants = [(word, variant_list) for word, variant_list in variants.items() if len(word) == word_length]
        max_variants = max(filtered_variants, key=lambda word: len(word[1]))
        max_num_variants = len(max_variants[1])

        # print(word_length, max_variants[0], len(max_variants[1]))
        if max_num_variants > 0:
            print(word_length)
            for word, variant_list in filtered_variants:
                if len(variant_list) == max_num_variants:
                    print(word, variant_list)


def find_most_swappable_letter(letter_swaps):
    letters = { letter: { 'total': 0} for letter in ascii_lowercase }
    
    for letter_pair, count in letter_swaps.items():
        letters[letter_pair[0]][letter_pair[1]] = count
        letters[letter_pair[1]][letter_pair[0]] = count
        letters[letter_pair[0]]['total'] += count
        letters[letter_pair[1]]['total'] += count

    return letters


def print_most_common_letter_swaps(letter_swaps, word_counts):
    for letter_pair, variants in sorted(letter_swaps.items(), key=lambda item: -len(item[1]))[:10]:
        variant_counts = { (word_1, word_2): word_counts[word_1] * word_counts[word_2] for word_1, word_2 in variants }
        most_common_count = max(variant_counts.values())
        most_common_variant = [word for word, count in variant_counts.items() if count == most_common_count][0]
        # freq = "{0:.2f}%".format(100 * sqrt(most_common_count) / total_words)
        freq = "{0:.2f}%, {1:.2f}%".format(100 * word_counts[most_common_variant[0]] / total_words,
                                           100 * word_counts[most_common_variant[1]] / total_words)

        print("<tr>")
        print(f"\t<td>{ letter_pair[0] } - { letter_pair[1] }</td>")
        print(f"\t<td>{ len(variants) }</td>")
        print(f"\t<td>{ ', '.join(most_common_variant) }</td>")
        print(f"\t<td>{ freq }</td>")
        print("</tr>")


def get_unswappable_pairs(letter_swaps):
    for i in range(25):
        for j in range(i + 1, 26):
            letter_pair = ascii_lowercase[i] + ascii_lowercase[j]
            if letter_pair not in letter_swaps:
                print(letter_pair)


def print_q_swap_words(letter_swaps):
    q_swaps = ["".join(sorted([letter, 'q'])) for letter in ascii_lowercase]

    for letter_pair in q_swaps:
        if letter_swaps.get(letter_pair):
            print(letter_swaps[letter_pair])


if __name__ == '__main__':
    # Get words
    # words = get_words_from_unix_dict()
    # words = set(get_word_list(os.path.join('word_lists', 'CROSSWD.TXT')))
    # words = set(get_word_list(os.path.join('word_lists', 'COMMON.TXT')))

    word_counts = get_word_counts(os.path.join('word_lists', 'filtered_word_counts.txt'))
    words = set(word_counts.keys())
    total_words = sum(word_counts.values())
    print(len(words))

    # Get vowel variants
    # variants = get_vowel_variants(words)
    # print(variants)
    # print(len(variants))
    # print_longest_variants(variants)

    # Show longest words that have a variant at each of its positions
    # all_position_variants = get_words_with_variants_at_each_position(words)
    # print_longest_word_with_variants_at_all_positions(all_position_variants, word_counts)

    # print_variant_counts('blander', word_counts)
    # word_log_frequencies = { word: log(count / total_words) for word, count in word_counts.items() }

    # Get all variants
    # variants = get_all_variants(words)
    # j_variants = get_variants_for_letter(words, 'j')
    # q_variants = get_variants_for_letter(words, 'q')

    # variant_distribution = get_distribution_of_variant_numbers(variants)
    # sum_of_variants = sum(number * count for number, count in variant_distribution.items())
    # print(variant_distribution)
    # print(sum_of_variants / len(words))

    # Get letter swaps
    letter_swaps = get_letter_to_letter_swaps(words)
    letter_swap_proportions = get_letter_swap_proportions(letter_swaps)
    print_most_swapped_letters(letter_swap_proportions)
    print_most_common_letter_each_letter_is_swapped_with(letter_swaps)

    # letter_counts = get_letter_counts(words)
    # print_proportion_of_words_with_swaps(letter_swap_proportions, letter_counts)
    # print_most_common_letter_to_swap_with_letter(letter_swap_proportions, letter_counts)

    # print_most_variants(variants, 30)
    # print_most_variants_for_word_length(variants, word_counts)
    # find_most_common_word_without_variants(word_counts, variants)
    # find_longest_word_without_variants(word_counts, variants)

    # print(len(variants.keys()))
    # print_longest_variants(variants)
    # print(variants['nationalizations'])

    #  TODO 
    #   for each letter, show which letter can most often replace it

    # Number of letter pairs that can be swapped (out of a possible 325 (25 * 26  /2))
    # print(len(list(letter_swaps.keys())))

    # get_unswappable_pairs(letter_swaps.keys())
    # print_q_swap_words(letter_swaps)
