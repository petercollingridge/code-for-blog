from fractions import Fraction


class Expression:
    def __init__(self, n, k=0, coefficient=1):
        self.terms = {(n, k): Fraction(coefficient)}
        self.constant = 0

    def __str__(self):
        s = " + ".join("{} * w({}, {})".format(
            coefficient,
            term[0],
            term[1]
        ) for term, coefficient in self.terms.items())

        if self.constant:
            s += " + {}".format(self.constant)

        return s

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
            new_term = (n, k + 2)
            p = coefficient * Fraction(v * (v - 2), d)
            self.add_term(new_term, p)
            self.constant += p
        
        # First turn match
        if k > 0:
            new_term = (n - 1, k - 1)
            p = coefficient * Fraction(k, u)
            self.add_term(new_term, p)
            self.constant += p

        # Novel match
        if k < n:
            new_term = (n - 1, k)
            p = coefficient * Fraction(v, d)
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


if __name__ == '__main__':
    exp = Expression(3, 0)
    exp.expand_term(3, 0)
    exp.expand_term(3, 2)

    
    print(exp)