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


def get_expected_numbers_of_turns_for_game_states(n):
    """
    Given n pairs, find all the game states in terms of
    (pairs to find, cards revealed) and find the expected number of turns
    to win the game from that state
    """
    decks = get_limited_decks(n)
    states = [get_game_states(deck) for deck in decks]
    turns = get_state_turn_counts(states)

    for state, turn_counts in turns.items():
        if state != '-':
            print(state, Fraction(sum(turn_counts) / len(turn_counts)).limit_denominator())


def get_distribution_of_turns_for_game_states(n):
    """
    Given n pairs, find all the game states in terms of
    (pairs to find, cards revealed) and find the expected number of turns
    to win the game from that state
    """
    decks = get_limited_decks(n)
    states = [get_game_states(deck) for deck in decks]
    turns_for_state = get_state_turn_counts(states)

    for delta in range(0, n):
        for pairs_to_go in range(0, n + 1):
            state = (pairs_to_go, pairs_to_go - delta)
            turn_counts = turns_for_state.get(state)

            if turn_counts:
                print(state)
                distribution = Counter(turn_counts)
                total = len(turn_counts)
                for turns, count in distribution.items():
                    print('  t = {}, p = {}'.format(turns, Fraction(count / total).limit_denominator()))


def get_state_transitions(states):
    """
    Given a list of game, where each game is a list of states,
    return a dict that maps a state to a Counter of the states that follow it.
    """

    transitions = defaultdict(Counter)

    for game in states:
        current_state = game[0]
        for next_state in game[1:]:
            transitions[current_state][next_state] += 1
            current_state = next_state
        transitions[current_state][(0, 0)] += 1

    return transitions


def get_new_states(n):
    previous_decks = get_limited_decks(n - 1)
    previous_states = {state for deck in previous_decks for state in get_game_states(deck)}
    new_decks = get_limited_decks(n)
    new_states = {state for deck in new_decks for state in get_game_states(deck) if state not in previous_states}
    print(new_states)


def get_game_state_tree(n):
    decks = get_limited_decks(n)
    states = [get_game_states(deck) for deck in decks]
    transitions = get_state_transitions(states)

    for state, transition in transitions.items():
        print(state)
        for next_state, count in transition.items():
            print("  => {}: {}".format(next_state, count))


def print_markov_chain(transitions):
    states = list(state for state in transitions.keys() if state != '-') + [(0, 0)]
    print("nodes = [{}]".format(', '.join("'{}'".format(state) for state in states if state != '-')))
    edges = "edges = ["

    for state_1, transition in transitions.items():
        if state_1 == '-':
            continue
        state_index_1 = states.index(state_1)
        for state_2, count in transition.items():
            if state_2 == '-':
                continue
            else:
                state_index_2 = states.index(state_2)
                edges += "({}, {}, {}), ".format(state_index_1, state_index_2, count)
        
    edges += "]"
    print(edges)


def get_expected_turns(n):
    """
    Get the expected number of turns for a game of n pairs by calculating
    the expected number of turns for every intermediate state.
    """

    expected_turns = dict()

    def get_expected_turns_for_state(n, k):
        state = (n, k)

        # If we have already calculated it, use that value
        if expected_turns.get(state) is not None:
            return expected_turns[state]

        # w(n, n) = n
        if n == k:
            return n

        u = n * 2 - k   # Number of uncovered cards

        # No known cards, so no chance of a match unless both cards are the same
        if k == 0:
            p1 = Fraction(1, u - 1)
            w = p1 * (1 + get_expected_turns_for_state(n - 1, k))
            p2 = Fraction(u - 2, u - 1)
            if p2 > 0:
                w += p2 * (1 + get_expected_turns_for_state(n, 2))
        else:
            # First turn match
            p1 = Fraction(k, u)
            w = p1 * (1 + get_expected_turns_for_state(n - 1, k - 1))

            d = u * (u - 1)
            if u - k > 0 and d > 0:
                # Novel match
                p2 = Fraction(u - k, d)
                if p2 > 0:
                    w += p2 * (1 + get_expected_turns_for_state(n - 1, k))
                
                # No match
                p3 = Fraction((u - k) * (u - k - 2), d)
                if p3 > 0:
                    w += p3 * (1 + get_expected_turns_for_state(n, k + 2))

                # Second turn match
                p4 = Fraction((u - k) * k, d)
                if p4 > 0:
                    w += p4 * (2 + get_expected_turns_for_state(n - 1, k))

        expected_turns[state] = w
        return w

    w = get_expected_turns_for_state(n, 0)
    # print(expected_turns)

    return w


def get_expected_turns_non_recursively(N):
    """
    Get the expected number of turns for a game of N pairs by calculating
    the expected number of turns for every intermediate state.
    """

    for n in range(N + 1):
        print(n)
        # w(n, k) = n
        new_w = [None] * (n + 1)
        new_w[n] = n

        for k in range(n, -1, -1):
            # Calculate w(n, k) in terms of w(n, k + 2), w(n - 1, k), w(n - 1, k - 1)
            w = 0
            u = n * 2 - k   # Number of uncovered cards
            d = u * (u - 1) # Denominator for uncovered cards over two turns
            v = u - k

            # No match
            if k + 2 <= n:
                # p = Fraction(v * (v - 2), d)
                p = v * (v - 2) / d
                w += p * (1 + new_w[k + 2])

            # Novel match
            if k < n:
                # p = Fraction(v, d)
                p = v / d
                w += p * (1 + old_w[k])

                # Second turn match
                if k:
                    w += k * p * (2 + old_w[k])

            # First turn match
            if k:
                # p = Fraction(k, u)
                p = k / u
                w += p * (1 + old_w[k - 1])

            new_w[k] = w

        old_w = new_w

    return new_w[0]


if __name__ == '__main__':
    n = 3


    # get_expected_numbers_of_turns(n)
    # get_distribution_of_turns(n)
    # get_expected_numbers_of_turns_for_game_states(n)
    # get_distribution_of_turns_for_game_states(n)
    # get_game_state_tree(n)
    # get_new_states(n)

    # for n in range(1, 100):
    # w = get_expected_turns(n)
    n = 20000
    w = get_expected_turns_non_recursively(n)
    print(w)
    # print(n, w.numerator / w.denominator / n)
    print(n, w / n)