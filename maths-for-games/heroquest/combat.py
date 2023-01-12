import random
import operator as op
from collections import defaultdict
from fractions import Fraction
from functools import reduce
from itertools import product


def n_choose_r(n, r):
    numerator = reduce(op.mul, range(n, n - r, -1), 1)
    denominator = reduce(op.mul, range(1, r + 1), 1)
    return numerator // denominator


class Character():
    def __init__(self, name, attack, defend, body):
        self.name = name
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
    def __init__(self, name, attack, defend, body):
        Character.__init__(self, name, attack, defend, body)
        self.type = 'hero'

    def _get_defense_prob(self):
        return Fraction(1, 3)


class Monster(Character):
    def __init__(self, name, attack, defend, body):
        Character.__init__(self, name, attack, defend, body)
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


def get_p_damage_on_leaving_combat_state(character1, character2):
    """
    For a combat state between character1 and character2, return the probabilities of
    damage given that at least one character dealt damage.
    The dictionary maps a 2-tuple of damage to the probability of that damage
    e.g. (1, 0): 0.5, means there is a 0.5 chance of character1 dealing 1 damage
         (0, 2): 0.2, means there is a 0.2 chance of character2 dealing 2 damage
    """

    attack1 = attack(character1, character2)
    attack2 = attack(character2, character1)
    p1 = attack1.get(0)
    p2 = attack2.get(0)

    # Probability that it's character1 that deals damage
    p_character_1_damage = Fraction(1 - p1, 1 - p1 * p2)
    p_character_2_damage = 1 - p_character_1_damage

    probs = {}
    # Factor to multiply probabilities given probs[0]
    # E.g. goblin has 3/9 chance of doing 1 damage and 1/9 chance of doing 2 damage each turn
    # If there is a 39/43 chance of doing 0 damage at the end, then there is a 4/43 chance of doing some damage
    # Which maps to 3/43 chance of doing 1 damage and 1/43 chance of doing 2 damage at the end
    r = Fraction(p_character_2_damage,  1 - p2)
    for n in range(1, character2.attack + 1):
        probs[(0, n)] = attack2.get(n, 0) * r

    r = Fraction(p_character_1_damage,  1 - p1)
    for n in range(1, character1.attack + 1):
        probs[(n, 0)] = attack1.get(n, 0) * r

    return probs


def get_probability_distribution_for_final_damage(character1, character2):
    """ 
    Return an array, where each item is the probability of character1
    having bps equal to the array index, when at the end of combat with character2
    """
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

    # To get final damage probability, multiply by probability of defender dealing 0 damage
    p_final_damage = [p_combat[bp] * p_damage[0] for bp in range(character1.body + 1)]
    # Except for when attacker has 0 bp and is dead
    p_final_damage[0] = p_combat[0]
    p_final_damage.reverse()
    return p_final_damage


def get_p_final_body_points(character1, character2):
    """
    Given a fight between character1 and character2, return a dict mapping
    a 2-tuple of the final body points to the probability of that result.

    e.g. (4, 0): 0.3 corresponds to a 0.3 chance that character1 ends with
    4 body points and character2 is dead.

    Note that one of the numbers in the tuple must always be 0 since one
    character must be dead for combat to have ended.
    """

    p_damage = get_p_damage_on_leaving_combat_state(character1, character2)

    # Map a 2-tuple representing a combat state to probability of entering that combat state
    # The 2-tuple represents (<bp of character1>, <bp of character2>)
    p_combat_state = defaultdict(int)

    # There is a 100% chance of starting with both characters at their starting bp
    p_combat_state[(character1.body, character2.body)] = 1

    # Fill in combat states starting with the one we know and expanding down, then
    for body1 in range(character1.body, 0, -1):
        for body2 in range(character2.body, 0, -1):
            # Probability of being in this state
            p_this_state = p_combat_state[(body1, body2)]

            # Update probabilities of next states
            for (damage1, damage2), p in p_damage.items():
                new_body1 = max(0, body1 - damage2)
                new_body2 = max(0, body2 - damage1)
                p_combat_state[(new_body1, new_body2)] += p_this_state * p
    
    # Filter to get just the combat states where one character is dead
    final_combat_states = {}
    for (bp1, bp2), p in p_combat_state.items():
        if bp1 == 0 or bp2 == 0:
            final_combat_states[(bp1, bp2)] = p

    return final_combat_states


def get_attack_stats(character1, character2):
    p_final_damage = get_probability_distribution_for_final_damage(character1, character2)
    p_monster_win = float(p_final_damage[-1])

    print(f"p(Monster wins) = {p_monster_win}")
    print(f"p(Monster wins) = 1 in {1 / p_monster_win}")
    print(f"E(damage to hero) = {float(get_expected_value(p_final_damage))}")

    for i, damage in enumerate(p_final_damage):
        print(character1.body - i, float(damage))


def get_expected_value(probabilities):
    """
    Given an array of probabilities, return the expected value,
    where the value of associated with each probability is its index.
    """

    expected_value = 0
    for i, p in enumerate(probabilities):
        expected_value += i * p
    return expected_value


def get_win_odds_table(heroes, monsters):
    """ For each pairing of hero and monster, show the odds that the monster wins """

    for hero, monster in product(heroes, monsters):
        p_final_damage = get_probability_distribution_for_final_damage(hero, monster)
        odds = round(1 / float(p_final_damage[-1]), 2)
        print(hero.name, monster.name, odds)


def get_expected_damage_table(heroes, monsters):
    """ For each pairing of hero and monster, show amount of damage
        the monster can expect to deal by the end of combat
    """

    for hero, monster in product(heroes, monsters):
        p_final_damage = get_probability_distribution_for_final_damage(hero, monster)
        e_damage = round(float(get_expected_value(p_final_damage)), 2)
        print(hero.name, monster.name, e_damage)


# Heroes
barbarian = Hero('barbarian', 3, 2, 8)
dwarf = Hero('dwarf', 2, 2, 7)
elf = Hero('elf', 2, 2, 6)
wizard = Hero('wizard', 1, 2, 4)

# Basic monsters (1 body point each)
goblin = Monster('goblin', 2, 1, 1)
skeleton = Monster('skeleton', 2, 2, 1)
zombie = Monster('zombie', 2, 3, 1)
orc = Monster('orc', 3, 2, 1)
fimir = Monster('fimir', 3, 3, 1)
mummy = Monster('mummy', 3, 4, 1)    # Same as Chaos warrior
gargoyle = Monster('gargoyle', 4, 4, 1)

# Ogres
ogre_warrior = Monster('ogre warrior', 5, 5, 3)
ogre_champion = Monster('ogre champion', 5, 5, 4)
ogre_chieftain = Monster('ogre chieftain', 6, 6, 4)
ogre_lord = Monster('ogre lord', 6, 6, 5)

# Monsters from the Frozen Horror
ice_gremlin = Monster('ice gremlin', 2, 3, 3)
yeti = Monster('yeti', 3, 3, 5)
warbear = Monster('warbear', 4, 4, 6)
frozen_horror = Monster('frozen horror', 5, 4, 6)
krag = Monster('krag', 5, 5, 4)

heroes = (barbarian, dwarf, elf, wizard)
monsters = (goblin, skeleton, zombie, orc, fimir, mummy, gargoyle)

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

# get_probability_distribution_for_final_damage(barbarian, goblin)
# print(barbarian.simulate_combat_probabilities(goblin, 1000000))

# get_attack_stats(wizard, gargoyle)

# print(wizard.simulate_combat_probabilities(gargoyle, 100000))
# print(barbarian.simulate_combat_probabilities(frozen_horror, 100000))

# get_expected_damage_table(heroes, monsters)
# get_win_odds_table(heroes, monsters)

# print(get_p_damage_on_leaving_combat_state(barbarian, goblin))
for state, p in get_p_final_body_points(barbarian, frozen_horror).items():
    print(state, float(p))
