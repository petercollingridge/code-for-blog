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

    # Probability of entering combat state of having x body points
    # There is a 100% probability of entering with the starting body points
    p_combat = {character1.body : 1}
    p_final_damage = [p_damage[0]]

    for body in range(character1.body - 1, -1, -1):
        # Probability of reaching this combat state
        p = 0
        for damage in range(1, character2.attack + 1):
            p += p_combat.get(body + damage, 0) * p_damage[damage]
        p_combat[body] = p
        p_final_damage.append(p * p_damage[0])

    print(f"p(Monster wins) = 1 in {float(1 / p_combat[0])}")
    print(f"E(damage to hero) = {float(get_expected_value(p_final_damage))}")

    print(float(p_combat[0]))
    print([float(d) for d in p_final_damage])
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

# get_probability_distribution_for_final_damage(barbarian, goblin)
# get_probability_distribution_for_final_damage(barbarian, gargoyle)
# get_probability_distribution_for_final_damage(wizard, goblin)
get_probability_distribution_for_final_damage(wizard, gargoyle)
