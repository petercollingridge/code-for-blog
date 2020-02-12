from fractions import Fraction
from collections import Counter, defaultdict
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


def get_game_states(deck):
    """
    Given a deck, return a list of game states, where a state is a tuple
    in the form (pairs to find, cards revealed)
    """

    pairs_to_find = len(deck) // 2
    states = []
    position = 0
    cards_seen = set()

    while pairs_to_find > 0:
        card = deck[position]
        position += 1
        states.append((pairs_to_find, len(cards_seen)))

        if card in cards_seen:
            # We know how to make a pair, so make one
            pairs_to_find -= 1
            cards_seen.remove(card)
        else:
            # Find a card we can't pair, so look at the next card
            next_card = deck[position]
            position += 1
            if next_card == card:
                # Got a pair
                pairs_to_find -= 1
            elif next_card in cards_seen:
                # We can make a pair on the next turn
                # Add dummy state
                states.append('-')
                pairs_to_find -= 1
                cards_seen.add(card)
                cards_seen.remove(next_card)
            else:
                # We did't make a pair, so remember what we have
                cards_seen.add(card)
                cards_seen.add(next_card)

    return states


def get_state_turn_counts(decks):
    turns = defaultdict(list)

    for deck in decks:
        turn = 1
        for state in deck[::-1]:
            turns[state].append(turn)
            turn += 1

    return turns


def get_expected_numbers_of_turns(n):
    """
    Given n pairs, print the expected number of turns to finish the game as a nice fraction.
    """
    decks = get_limited_decks(n)
    turns = [play_game(deck) for deck in decks]
    print(Fraction(sum(turns) / len(decks)).limit_denominator())


def get_distribution_of_turns(n):
    """
    Given n pairs, show the distibution of turns.
    e.g. with 3 pairs, 1 game will take 3 turns,
    8 games will take 4 turns and 6 games will take 5 turns.
    """

    decks = get_limited_decks(n)
    turns = [play_game(deck) for deck in decks]
    turn_distribution = Counter(turns)
    
    for n_turns in turn_distribution.keys():
        print("{} turns: {} games".format(n_turns, turn_distribution[n_turns]))
    
    print("Total decks = n!! = {}".format(len(decks)))


def main():
    get_expected_numbers_of_turns(4)
    # get_distribution_of_turns(4)

    # # states = get_game_states('ABCDEFABCDEF')
    # # print(states)

    # print(len(decks))
    # states = [get_game_states(deck) for deck in decks]
    # turns = get_state_turn_counts(states)

    # for state, turn_counts in turns.items():
    #     print(state, sum(turn_counts) / len(turn_counts))
    #     # print(state, Counter(turn_counts))


if __name__ == '__main__':
    main()
