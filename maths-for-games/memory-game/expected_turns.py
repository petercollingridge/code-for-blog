from math import floor
from fractions import Fraction

def expected_turns_without_a_match(n):
    """
    Calculate the expected number of turns without getting a match, given <n> pairs.
    """

    result = 0
    numerator = 0
    denominator = 2 * n
    for i in range(floor(n / 2)):
        p1 = (1 - Fraction(numerator, denominator))
        p2 = (1 - Fraction(numerator + 1, denominator - 1))
        result += (i + 1) * p1 * p2
        numerator += 2
        denominator -= 2

    return result


def difference_in_expected_values(n):
    e1 = expected_turns_without_a_match(n)
    e2 = expected_turns_without_a_match(n - 2)
    return (e1 - e2) / 2

d = difference_in_expected_values(6)
print(d, float(d))
