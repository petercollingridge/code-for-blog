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


if __name__ == '__main__':
    exp = Expression(3, 0)
    exp.expand_term(3, 0)
    exp.expand_term(3, 2)
    print(exp)

    exp = Expression(4, 0)
    exp.expand_term(4, 0)
    exp.expand_term(4, 2)
    exp.expand_term(3, 1)
    exp.expand_term(3, 2)

    print(exp)