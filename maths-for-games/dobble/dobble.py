import string
import math
from itertools import combinations

n = 6   # Total number of symbols
s = 3   # Number of symbols per card
symbols = string.uppercase[:n]


# Given a string of symbols and integer s,
# return a list of all combinations of symbols of length s
# Given (ABC, 2), return [AB, AC, BC]
def get_card(remaining_symbols, s):
    s -= 1

    if s == 0:
        return remaining_symbols

    cards = []
    for i in range(len(remaining_symbols) - 1):
        symbol = remaining_symbols[i]
        suffixes = get_card(remaining_symbols[i + 1:], s)
        cards += [symbol + suffix for suffix in suffixes]

    return cards

# Similar to get_card, but cards must match exactly symbol on existing_cards
# Given 2, return [AC, BC]
def get_dobble_card(s, remaining_symbols, unmatched_cards):
    s -= 1

    cards = []
    for index, symbol in enumerate(remaining_symbols):
        # Get set of cards which contain this symbol
        new_unmatched_cards = []
        new_remaining_symbols = remaining_symbols[index + 1:]

        for card in unmatched_cards:
            if symbol in card:
                new_remaining_symbols = [other_symbol for other_symbol in new_remaining_symbols if other_symbol not in card]
            else:
                new_unmatched_cards.append(card)

        if s > 0:
            next_symbols = get_dobble_card(s, new_remaining_symbols, new_unmatched_cards)
            cards += [symbol + next_symbol for next_symbol in next_symbols]
        elif not new_unmatched_cards:
            cards.append(symbol)

        # cards.add(tuple(tuple(symbol + next_symbol) for next_symbol in next_symbols))

    return cards

def get_dobble_deck(symbols_per_card, symbols, deck):
    # Get cards that work with this deck
    cards = get_dobble_card(symbols_per_card, symbols, deck)

    # If it's not possible to add more cards, check this we have a valid deck
    # Are all symbols used and there is not a single symbol common to all cards
    if not cards:
        if set(symbols) == set(symbol for card in deck for symbol in card) and \
            not set.intersection(*[set(card) for card in deck]):
                return [deck]
        else:
            # Not a valid deck, so return nothing
            return []

    all_decks = []
    for card in cards:
        # Find decks that can be created with each new card
        for new_deck in get_dobble_deck(symbols_per_card, symbols, deck + [card]):
            all_decks.append(new_deck)

    return all_decks

# for n in range(3, 10):
#     symbols = string.uppercase[:n]
#     s = int(math.ceil((1 + math.sqrt(4 * n - 3)) / 2))
#     print(n, s)
#     decks = get_dobble_deck(s, symbols, [symbols[:s]])
#     if decks:
#         max_size = max(len(deck) for deck in decks)
#         print(max_size)
#         print(decks[0])

symbols = string.uppercase[:12]
s = 4
decks = get_dobble_deck(s, symbols, [symbols[:s]])
max_size = max(len(deck) for deck in decks)
print(max_size)
print(decks[0])

# cards = get_dobble_card(s, symbols, ['ABC', ['ADE']])
# cards = get_dobble_card(3, 'ABCDEFG', ['ABC', 'ADE', 'AFG', 'BDF'])
