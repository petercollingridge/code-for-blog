from fractions import Fraction
from collections import Counter
from itertools import permutations
from string import ascii_uppercase


def get_all_decks(n):
    """ Return all permutations of n pairs of cards. """

    alphabet = ascii_uppercase[:n]
    cards = alphabet * 2
    decks = list(permutations(cards, n * 2))
    return decks


def get_limited_decks(n):
    """ Get all possible decks of n pair, where the first A is before the first B, and so on. """
    alphabet = ascii_uppercase[:n]
    num_cards = 2 * n
    decks = [{}]

    for card in alphabet:
        new_decks = []

        # Add card to the first empty position in each existing deck
        for deck in decks:
            for i in range(num_cards):
                if deck.get(i) is None:
                    deck[i] = card
                    break

            # Add a second card at every empty space
            for i in range(num_cards):
                if deck.get(i) is None:
                    new_deck = deck.copy()
                    new_deck[i] = card
                    new_decks.append(new_deck)
        
        decks = new_decks

    # Convert objects into strings of cards
    string_decks = []
    for deck in decks:
        string_decks.append("".join(deck[i] for i in range(num_cards)))

    return string_decks


def play_game(deck):
    """
    Given a deck, return the number of turns it takes to complete a game
    if you reveal the cards in order.
    """

    pairs_to_find = len(deck) / 2
    turns = 0
    position = 0
    cards_seen = set()

    while pairs_to_find > 0:
        card = deck[position]
        turns += 1
        position += 1

        # print(turns, "Pick card", card)

        if card in cards_seen:
            # We know how to make a pair, so make one
            # print("Make a pair")
            pairs_to_find -= 1
            cards_seen.remove(card)
        else:
            # Find a card we can't pair, so look at the next card
            next_card = deck[position]
            position += 1
            # print("Pick second card", next_card)

            if next_card == card:
                # Got a pair
                # print("Make a pair with second card")
                pairs_to_find -= 1
            elif next_card in cards_seen:
                # We can make a pair on the next turn
                # print("Make a pair next turn")
                turns += 1
                pairs_to_find -= 1
                cards_seen.add(card)
                cards_seen.remove(next_card)
            else:
                # We did't make a pair, so remember what we have
                # print("No pair")
                cards_seen.add(card)
                cards_seen.add(next_card)

    return turns


def main():
    # decks = get_all_decks(4)
    decks = get_limited_decks(8)
    turns = [play_game(deck) for deck in decks]
    print(Counter(turns))
    print(Fraction(sum(turns) / len(decks)).limit_denominator())


if __name__ == '__main__':
    main()
