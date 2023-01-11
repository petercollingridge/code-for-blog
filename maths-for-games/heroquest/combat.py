import random
import operator as op
from collections import defaultdict
from fractions import Fraction
from functools import reduce


def n_choose_r(n, r):
    numerator = reduce(op.mul, range(n, n - r, -1), 1)
    denominator = reduce(op.mul, range(1, r + 1), 1)
    return numerator // denominator


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
            p = n_choose_r(dice, n) * (probability ** n) * ((1 - probability) ** (dice - n))
            probabilities.append((n, p))
        return probabilities

    def simulate_combat_probabilities(self, other, n):
        """
        Simulation fighting another character n times
        and return the distribution of this character's
        body points at the end of combat.
        """
        final_body_points = defaultdict(int)

        for _ in range(n):
            body_points = self.simulate_combat(other)
            final_body_points[body_points] += 1

        # Convert counts to probabilities
        for body in final_body_points:
            final_body_points[body] /= n

        return final_body_points

    def simulate_combat(self, other):
        self_body = self.body
        other_body = other.body
        self_defense_p = float(self._get_defense_prob())
        other_defense_p = float(other._get_defense_prob())

        # Each loop is one round of combat
        while True:
            # Self attacks other
            attack = sum(random.random() < 0.5 for _ in range(self.attack))
            defend = sum(random.random() < other_defense_p for _ in range(other.defend))
            damage = max(0, attack - defend)
            other_body -= damage
            if other_body <= 0:
                return self_body

            # Other attacks self
            attack = sum(random.random() < 0.5 for _ in range(other.attack))
            defend = sum(random.random() < self_defense_p for _ in range(self.defend))
            damage = max(0, attack - defend)
            self_body -= damage
            if self_body <= 0:
                return 0

    def simulate_attack(self, other):
        attack = sum(random.random() < 0.5 for _ in range(self.attack))
        defend = sum(random.random() < other._get_defense_prob() for _ in range(other.defend))
        return max(0, attack - defend)



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


def attack(character1, character2):
    """ Return probabilities for the damage dealt by character1 attacks character2 """

    attack = character1.get_attack_probabilities()
    defence = character2.get_defence_probabilities()

    probabilities = defaultdict(int)
    for attack_n, attack_p in attack:
        for defend_n, defend_p in defence:
            damage = max(0, attack_n - defend_n)
            probabilities[damage] += attack_p * defend_p
    return probabilities


def get_prob_dist_for_damage_on_leaving_combat_state(character1, character2):
    """
    If character1 attacks character2 and character2 has 1 body point.
    Return the probability distribution for the amount of damage will take 
    on leaving this combat state.
    If they take 0 damage, then character2 has been killed.
    """

    attack1 = attack(character1, character2)
    attack2 = attack(character2, character1)
    p1 = attack1.get(0)
    p2 = attack2.get(0)

    probs = {0 : Fraction(1 - p1, 1 - p1 * p2)}
    # Factor to multiply probabilities given probs[0]
    # E.g. goblin has 3/9 chance of doing 1 damage and 1/9 chance of doing 2 damage each turn
    # If there is a 39/43 chance of doing 0 damage at the end, then there is a 4/43 chance of doing some damage
    # Which maps to 3/43 chance of doing 1 damage and 1/43 chance of doing 2 damage at the end
    r = (1 - probs[0]) / (1 - p2)

    for n in range(1, character2.attack + 1):
        probs[n] = attack2.get(n, 0) * r

    return probs


def get_probability_distribution_for_final_damage(character1, character2):
    p_damage = get_prob_dist_for_damage_on_leaving_combat_state(character1, character2)

    # Map number of bps to probability of entering combat with that num of body points
    p_combat = defaultdict(int)

    # There is a 100% probability of entering with the starting body points
    p_combat[character1.body] = 1

    for body in range(character1.body, 0, -1):
        p_this_state = p_combat[body]

        for damage in range(1, character2.attack + 1):
            new_body = max(0, body - damage)
            p_combat[new_body] += p_this_state * p_damage[damage]

    p_final_damage = [p_combat[bp] * p_damage[0] for bp in range(character1.body + 1)]
    p_final_damage.reverse()

    print(f"p(Monster wins) = 1 in {float(1 / p_combat[0])}")
    print(f"E(damage to hero) = {float(get_expected_value(p_final_damage))}")

    print(float(p_combat[0]))
    for i, damage in enumerate(p_final_damage):
        print(character1.body - i, float(damage))
    print(float(sum(p_final_damage)))


def get_expected_value(probabilities):
    expected_value = 0
    for i, p in enumerate(probabilities):
        expected_value += i * p
    return expected_value

barbarian = Hero(3, 2, 8)
dwarf = Hero(2, 2, 7)
elf = Hero(2, 2, 6)
wizard = Hero(1, 2, 4)

goblin = Monster(2, 1, 1)
skeleton = Monster(2, 2, 1)
zombie = Monster(2, 3, 1)
orc = Monster(3, 2, 1)
fimir = Monster(3, 3, 1)
mummy = Monster(3, 4, 1)        # Same as Chaos warrior
gargoyle = Monster(4, 4, 1)

# print(barbarian.get_attack_probabilities())
# print(barbarian.get_defence_probabilities())
# print(goblin.get_attack_probabilities())
# print(goblin.get_defence_probabilities())

# print(attack(barbarian, goblin))
# print(attack(goblin, barbarian))
# print(attack(barbarian, gargoyle))
# print(get_prob_of_0_damage(barbarian, goblin))

# get_probability_distribution_for_final_damage(barbarian, gargoyle)
# get_probability_distribution_for_final_damage(wizard, goblin)
# get_probability_distribution_for_final_damage(wizard, gargoyle)

get_probability_distribution_for_final_damage(barbarian, goblin)
# print(barbarian.simulate_combat_probabilities(goblin, 1000000))
