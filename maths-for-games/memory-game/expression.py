from fractions import Fraction


class Expression:
    def __init__(self, terms=None, constant=0):
        if terms is None:
            self.terms = {}
        elif isinstance(terms, tuple):
            self.terms = {terms: 1}
        else:
            self.terms = terms
        self.constant = constant

    def __str__(self):
        s = " + ".join("{} * w({}, {})".format(
            coefficient,
            term[0],
            term[1]
        ) for term, coefficient in self.terms.items())

        if self.constant:
            s += " + {}".format(self.constant)

        return s

    def __add__(self, other):
        total = Expression()
        total.constant = self.constant + other.constant

        for term, coefficient in self.terms.items():
            total.add_term(term, coefficient)

        for term, coefficient in other.terms.items():
            total.add_term(term, coefficient)

        return total

    def __sub__(self, other):
        total = Expression()
        total.constant = self.constant - other.constant

        for term, coefficient in self.terms.items():
            total.add_term(term, coefficient)

        for term, coefficient in other.terms.items():
            total.add_term(term, -coefficient)

        return total

    def expand_term(self, n, k):
        term = (n, k)
        coefficient = self.terms.get(term)
        if not coefficient:
            print('Not such term {}'.format(term))
            return

        # Remove this term
        del self.terms[term]

        # Handy values
        u = n * 2 - k   # Number of uncovered cards
        d = u * (u - 1) # Denominator for uncovered cards over two turns
        v = u - k

        # No match
        if k + 2 <= n:
            p = coefficient * Fraction(v * (v - 2), d)

            if k + 2 == n:
                self.constant += p * (n + 1)
            else:
                new_term = (n, k + 2)
                self.add_term(new_term, p)
                self.constant += p
        
        # First turn match
        if k > 0:
            p = coefficient * Fraction(k, u)
            new_term = (n - 1, k - 1)
            self.add_term(new_term, p)
            self.constant += p

        # Novel match
        if k < n:
            p = coefficient * Fraction(v, d)
            if k + 1 == n:
                self.constant += p * n
            else:    
                new_term = (n - 1, k)
                self.add_term(new_term, p)
                self.constant += p

                # Second turn match
                if k > 0:
                    p *= k
                    self.add_term(new_term, p)
                    self.constant += p * 2

    def add_term(self, term, coefficient):
        current_coefficient = self.terms.get(term, 0)
        self.terms[term] = current_coefficient + coefficient


def get_state_in_lower_state(n, d=1):
    """ Get an expression for w(n, 0) in terms if w(n - d, i) for i = 0 to n - d. """

    exp = Expression((n, 0))
    for i in range(0, n + 1, 2):
        exp.expand_term(n, i)

    return exp

if __name__ == '__main__':
    # x = Expression({ (3, 2): 2 })
    # y = Expression({ (3, 2): Fraction(1, 2), (5, 1): Fraction(1, 3) })
    # print(x + y)
    # print(y - x)

    # w_3_0 = Expression((3, 0))
    # w_3_0.expand_term(3, 0)
    # w_3_0.expand_term(3, 2)
    # print(w_3_0)

    w_4_0 = Expression((4, 0))
    w_4_0.expand_term(4, 0)
    w_4_0.expand_term(4, 2)
    # w_4_0.expand_term(3, 1)
    # w_4_0.expand_term(3, 2)
    print(w_4_0)

    # w_4_2 = Expression((4, 2))
    # w_4_2.expand_term(4, 2)
    # print(w_4_2)
    # print(w_4_0 - w_3_0)

    # w_5_0 = get_state_in_lower_state(5)
    # print(w_5_0)