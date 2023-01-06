import operator as op
from fractions import Fraction
from functools import reduce

def ncr(n, r):
    numer = reduce(op.mul, range(n, n - r, -1), 1)
    denom = reduce(op.mul, range(1, r + 1), 1)
    return numer // denom

class Character():
    def __init__(self, attack, defend, body):
        self.attack = attack
        self.defend = defend
        self.body = body

    def get_attack_probabilities(self):
        p_attack = Fraction(1, 2)
        return self._get_probability_densities(self.attack, p_attack)

    def get_defence_probabilities(self):
        p_defend = self._get_defense_prob()
        return self._get_probability_densities(self.defend, p_defend)

    def _get_probability_densities(self, dice, probability):
        probabilities = []
        for n in range(0, dice + 1):
            p = ncr(dice, n) * (probability ** n) * ((1 - probability) ** (dice - n))
            probabilities.append((n, p))
        return probabilities


class Hero(Character):
    def __init__(self, attack, defend, body):
        Character.__init__(self, attack, defend, body)
        self.type = 'hero'

    def _get_defense_prob(self):
        return Fraction(1, 3)


class Monster(Character):
    def __init__(self, attack, defend, body):
        Character.__init__(self, attack, defend, body)
        self.type = 'monster'

    def _get_defense_prob(self):
        return Fraction(1, 6)




barbarian = Hero(3, 2, 8)
goblin = Monster(2, 1, 1)

print(barbarian.get_attack_probabilities())
print(barbarian.get_defence_probabilities())
print(goblin.get_attack_probabilities())
print(goblin.get_defence_probabilities())
