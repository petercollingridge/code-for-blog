from random import random, gammavariate

POPULATION_SIZE = 1000

# Get fitness of initial population
population = [gammavariate(2, 0.5) for _ in range(POPULATION_SIZE)]

# Calculate which individual reproduce
new_population = []
for index, fitness in enumerate(population):
    p = fitness / (fitness + 1)

    while random() < p:
        new_population.append(index)

print(sum(population))
print(len(new_population))
