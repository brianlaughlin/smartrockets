import random

import constants
from rocket import Rocket


class population():
    def __init__(self, pop_size):
        self.rockets = []
        self.pop_size = pop_size
        self.mating_pool = []
        self.generation = 1

        self.rockets.extend(Rocket(constants.WHITE) for _ in range(pop_size))

    def evaluate(self):
        """
        Evaluate the fitness of each rocket
        I uses the distance from the rocket to moon as fitness
        1 would mean that the rocket is at the moon
        """
        max_fitness = 0
        for rocket in self.rockets:
            rocket.calculate_fitness()
            if rocket.fitness > max_fitness:
                max_fitness = rocket.fitness
                print(f"Max Fitness : {max_fitness}")

        """
        normalize fitness
        if the fitness is higher than 1, it will be 1
        if the fitness is lower than 1, it will be 0
        """
        for rocket in self.rockets:
            # make sure we handle division by 0
            if max_fitness != 0:
                rocket.fitness /= max_fitness

        # create a mating pool
        self.mating_pool = []
        for rocket in self.rockets:
            n = int(rocket.fitness * 100)
            # add rocket to the mating pool n times
            self.mating_pool.extend(rocket for _ in range(n))  # add rocket to the mating pool n times

    def selection(self):
        # create a new population
        new_population = []
        # pick two parents from the mating pool
        for _ in range(self.pop_size):
            parent_a = random.choice(self.mating_pool)
            parent_b = random.choice(self.mating_pool)
            # create a child rocket
            child = parent_a.dna.crossover(parent_b.dna)
            child.mutate()
            new_population.append(Rocket(constants.WHITE, child))

        self.rockets = new_population
        self.generation += 1

    def run(self, WIN, life_counter):
        for i in range(self.pop_size):
            self.rockets[i].update(life_counter)
            self.rockets[i].show(WIN)