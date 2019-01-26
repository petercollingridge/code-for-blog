def get_word_counts(filepath):
    word_counts = dict()

    with open(filepath, 'r') as f:
        for line in f:
            temp = line.split('\t')
            if len(temp) > 1:
                word_counts[temp[0]] = int(temp[1])

    return word_counts


def show_in_order(counts):
    for item in sorted(counts.items(), key=lambda item: -item[1]):
        print("{}: {}".format(*item))


if __name__ == '__main__':
    import os
    word_counts = get_word_counts(os.path.join('word_lists', 'filtered_word_counts.txt'))
    
    print(word_counts['the'])
    print(word_counts.popitem())
