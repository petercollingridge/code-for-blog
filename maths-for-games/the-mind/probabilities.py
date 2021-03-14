from fractions import Fraction

# Probabilities for consecutive cards with two cards
p2 = Fraction(2, 100) * Fraction(1, 99) + Fraction(98, 100) * Fraction(2, 99)

# Start with the probability of getting consecutive cards with 2 cards
p3 = p2

# If One card is at the end and the other card is at the opposite end (i.e. 1 and 100),
# or the other card is one card away (e.g. 1 and 3), then there are two spaces to
# make a consecutive card
p3 += Fraction(1, 50) * Fraction(2, 99) * Fraction(2, 98)

# If cards have a gap of 1, but are not at the end (e.g. 2 and 4)
# then there are three spaces to make a consecutive card
p3 += 2 * Fraction(96, 100) * Fraction(1, 99) * Fraction(3, 98)

# Otherwise there are four spaces to go
p3 += (1 - Fraction(1, 50) * Fraction(2, 99) - 2 * Fraction(96, 100) * Fraction(1, 99)) * Fraction(4, 98)
 
print(p2)
print(p3)
print(float(p3))

for i in range(2, 11):
    p = sum(2 * n / (100 - n) for n in range(1, i))
    print(i, p)
