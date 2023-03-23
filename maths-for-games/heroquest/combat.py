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
        return self._get_success_probabilities(self.attack, p_attack)

    def get_defence_probabilities(self):
        p_defend = self._get_defense_prob()
        return self._get_success_probabilities(self.defend, p_defend)

    def _get_success_probabilities(self, num_dice, p_success):
        """
        When rolling num_dice dice, where each has <p_success> chance of success
        return a dict mapping number of successes to its probability.
        """
    
        probabilities = {}
        for n in range(0, num_dice + 1):
            p = n_choose_r(num_dice, n) * (p_success ** n) * ((1 - p_success) ** (num_dice - n))
            probabilities[n] = p
        return probabilities

    def get_damage_probabilities(self, other):
        """ Return probabilities for the damage dealt by character1 attacks character2 """

        attack = self.get_attack_probabilities()
        defence = other.get_defence_probabilities()

        probabilities = defaultdict(int)
        for attack_n, attack_p in attack.items():
            for defend_n, defend_p in defence.items():
                damage = max(0, attack_n - defend_n)
                probabilities[damage] += attack_p * defend_p
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
                return (self_body, 0)

            # Other attacks self
            attack = sum(random.random() < 0.5 for _ in range(other.attack))
            defend = sum(random.random() < self_defense_p for _ in range(self.defend))
            damage = max(0, attack - defend)
            self_body -= damage
            if self_body <= 0:
                return (0, other_body)

    def simulate_attack(self, other):
        attack = sum(random.random() < 0.5 for _ in range(self.attack))
        defend = sum(random.random() < other._get_defense_prob() for _ in range(other.defend))
        return max(0, attack - defend)


class Hero(Character):
    def __init__(self, name, attack, defend, body):
        super().__init__(name, attack, defend, body)
        self.type = 'hero'

    def _get_defense_prob(self):
        return Fraction(1, 3)


class Monster(Character):
    def __init__(self, name, attack, defend, body):
        super().__init__(name, attack, defend, body)
        self.type = 'monster'

    def _get_defense_prob(self):
        return Fraction(1, 6)


class Warbear(Monster):
    def __init__(self, name, attack, defend, body):
        super().__init__(name, attack, defend, body)

    def get_damage_probabilities(self, other):
        p = super().get_damage_probabilities(other)

        # Combine two lots of p to get final probabilities
        final_p = defaultdict(int)
        for damage1, p1 in p.items():
            for damage2, p2 in p.items():
                final_p[damage1 + damage2] += p1 * p2
        return final_p


class TestCharacter(Character):
    """ Character for use in testing function """
    def __init__(self, name, attack, defend, body, probabilities):
        super().__init__(name, attack, defend, body)
        self.type = 'test'
        self.probabilities = probabilities

    def get_damage_probabilities(self, _):
        return self.probabilities


def write_probabilities(probabilities, as_float=False):
    """
    Given a dict mapping values to their probabilities,
    print each value in order with its probability.
    If as_float is true, write as a float, otherwise 
    it will be written as stored (probably a Fraction).
    """
    for value in sorted(probabilities):
        p = probabilities[value]
        if as_float:
            p = float(p)
        print(value, p)


def get_expected_value(probabilities):
    """
    Given a dict mapping value to its probability, return the expected value.
    """

    return sum(value * p for value, p in probabilities.items())


def get_prob_dist_for_damage_on_leaving_combat_state(character1, character2):
    """
    DEFUNCT
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

    p_damage_1 = character1.get_damage_probabilities(character2)
    p_damage_2 = character2.get_damage_probabilities(character1)
    p1 = p_damage_1[0]
    p2 = p_damage_2[0]

    # Probability that both characters miss so we loop back round
    p_loop = p1 * p2

    # Probability that it's character1 that deals damage
    p_character_1_damage = Fraction(1 - p1, 1 - p_loop)
    p_character_2_damage = 1 - p_character_1_damage

    probs = {}

    # Update probabilities that the active character deals damage
    # e.g. when the barbarians attacks the goblin, r_active = 48/43
    r_active = Fraction(1, 1 - p_loop)
    for damage, p in p_damage_1.items():
        if damage > 0:
            probs[(damage, 0)] = p * r_active

    # Factor to multiply probabilities given probs[0]
    # E.g. goblin has 3/9 chance of doing 1 damage and 1/9 chance of doing 2 damage each turn
    # If there is a 39/43 chance of doing 0 damage at the end, then there is a 4/43 chance of doing some damage
    # Which maps to 3/43 chance of doing 1 damage and 1/43 chance of doing 2 damage at the end
    r = Fraction(p_character_2_damage,  1 - p2)
    for damage, p in p_damage_2.items():
        if damage > 0:
            probs[(0, damage)] = p * r

    return probs


def get_p_final_body_points(character1, character2):
    """
    Given a fight between character1 and character2, return a dict mapping
    a 2-tuple of the final body points to the probability of that result.

    e.g. (4, 0): 0.3 corresponds to a 0.3 chance that character1 ends with
    4 body points and character2 is dead.

    Note that one of the numbers in the tuple must always be 0 since one
    character must be dead for combat to have ended.
    """

    p_damage_1 = get_p_damage_on_leaving_combat_state(character1, character2)
    p_damage_2 = get_p_damage_on_leaving_combat_state(character2, character1)

    # Map a 3-tuple representing a combat state to probability of entering that combat state
    # The 3-tuple represents (<Which player's turn it is>, <bp of character1>, <bp of character2>)
    p_combat_state = defaultdict(int)

    # There is a 100% chance of starting with both characters at their starting bp
    p_combat_state[(1, character1.body, character2.body)] = 1

    # Fill in combat states starting with the one we know and expanding down, then
    for body2 in range(character2.body, 0, -1):
        for body1 in range(character1.body, 0, -1):
            for turn in (1, 2):
                # Probability of being in this state
                p_this_state = p_combat_state[(turn, body1, body2)]

                if p_this_state:
                    p_damage = p_damage_1 if turn == 1 else p_damage_2
                    # Update probabilities of next states
                    for damage, p in p_damage.items():
                        if turn == 1:
                            (damage1, damage2) = damage
                        else:
                            (damage2, damage1) = damage
                            
                        # If it's a player's turn and they dealt damage, then swap turns
                        if (turn == 1 and damage1 > 0) or (turn == 2 and damage2 > 0):
                            next_turn = 3 - turn
                        else:
                            next_turn = turn
                        
                        new_body1 = max(0, body1 - damage2)
                        new_body2 = max(0, body2 - damage1)
                        p_combat_state[(next_turn, new_body1, new_body2)] += p_this_state * p

    # Filter to get just the combat states where one character is dead
    final_combat_states = {}
    for (_, bp1, bp2), p in p_combat_state.items():
        # print((_, bp1, bp2), p)
        if bp1 == 0 or bp2 == 0:
            final_combat_states[(bp1, bp2)] = p

    return final_combat_states


def get_win_odds_table(heroes, monsters):
    """ For each pairing of hero and monster, show the odds that the monster wins """

    for hero, monster in product(heroes, monsters):
        p_final_bp = get_p_final_body_points(hero, monster)
        p_win = sum(p for (hero_bp, _), p in p_final_bp.items() if hero_bp > 0)
        odds_win = round(1 / float(1 - p_win), 2)
        print(hero.name, monster.name, odds_win)


def get_expected_damage_table(heroes, monsters):
    """ For each pairing of hero and monster, show amount of damage
        the monster can expect to deal by the end of combat
    """

    for hero, monster in product(heroes, monsters):
        p_final_bp = get_p_final_body_points(hero, monster)
        e_damage = 0
        for (hero_bp, _), p in p_final_bp.items():
            e_damage += (hero.body - hero_bp) * p
        print(hero.name, monster.name, round(float(e_damage), 2))


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
frozen_horror = Monster('frozen horror', 5, 4, 6)
krag = Monster('krag', 5, 5, 4)
warbear = Warbear('warbear', 4, 4, 6)

heroes = (barbarian, dwarf, elf, wizard)
monsters = (goblin, skeleton, zombie, orc, fimir, mummy, gargoyle)

# Goblin with 2 body points for testing purposes
goblin2 = Monster('goblin', 2, 1, 2)
test_char_1 = TestCharacter('Test 1', 0, 0, 2, {0: Fraction(1, 4), 1: Fraction(1, 2), 2: Fraction(1, 4)})
test_char_2 = TestCharacter('Test 2', 0, 0, 2, {0: Fraction(1, 2), 1: Fraction(1, 3), 2: Fraction(1, 6)})

# get_p_final_body_points(test_char_1, test_char_2)

# write_probabilities(barbarian.get_attack_probabilities())
# write_probabilities(barbarian.get_defence_probabilities())
# write_probabilities(goblin.get_attack_probabilities())
# write_probabilities(goblin.get_defence_probabilities())

# write_probabilities(barbarian.get_damage_probabilities(goblin))
# write_probabilities(barbarian.simulate_combat_probabilities(goblin2, 100000))
# print()
# for state, p in get_p_final_body_points(barbarian, goblin2).items():
#     print(state, float(p))

# write_probabilities(get_p_damage_on_leaving_combat_state(barbarian, goblin))
# write_probabilities(get_p_damage_on_leaving_combat_state(goblin, barbarian))
# write_probabilities(get_p_final_body_points(barbarian, goblin), True)
# write_probabilities(get_p_final_body_points(barbarian, gargoyle), True)

# get_expected_damage_table(heroes, monsters)
# get_win_odds_table(heroes, monsters)

# print(get_p_damage_on_leaving_combat_state(barbarian, goblin))
# for state, p in get_p_final_body_points(barbarian, frozen_horror).items():
#     print(state, float(p))

# write_probabilities(barbarian.get_damage_probabilities(warbear))
# write_probabilities(warbear.get_damage_probabilities(barbarian), 1)
# print(get_expected_value(barbarian.get_damage_probabilities(warbear)))
# write_probabilities(get_p_final_body_points(barbarian, warbear), True)