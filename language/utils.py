def get_word_counts(filepath):
    word_counts = dict()

    with open(filepath, 'r') as f:
        for line in f:
            temp = line.split('\t')
            if len(temp) > 1:
                word_counts[temp[0]] = int(temp[1])

    return word_counts


def show_in_order(counts, max_count=-1):
    for index, item in enumerate(sorted(counts.items(), key=lambda item: -item[1])):
        print("{}: {}".format(*item))
        if index == max_count:
            break


def convert_counts_to_percentages(counts, total=None):
    if not total:
        total = sum(value for value in counts.values())
    
    return { key: value * 100.0 / total for key, value in counts.items() }


if __name__ == '__main__':
    import os
    word_counts = get_word_counts(os.path.join('word_lists', 'filtered_word_counts.txt'))
    
    print(word_counts['the'])
    print(word_counts.popitem())
