def get_words(filename):
    """ Given a filename to a list of words, return a list of 5-letter words. """

    words = []
    with open(filename, 'r') as f:
        for line in f:
            words.append(line.strip())

    return words
