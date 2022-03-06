import random

from pygame import math as math

import constants


class DNA():
    def __init__(self, genes=None):
        if genes is None:
            self.genes = []

            for _ in range(constants.LIFESPAN):
                a, b = (math.Vector2(random.randint(-1, 1), random.randint(-1, 1)))

                # change magnitude of the vector to 0.1
                a *= 0.2
                b *= 0.2
                self.genes.append((a, b))
        else:
            self.genes = genes

    def crossover(self, partner):
        """
        Take half of the genes from the partner
        return new DNA(new_genes)
        """
        mid = len(self.genes) // 2
        new_genes = [self.genes[i] for i in range(mid)]
        new_genes.extend(partner.genes[i] for i in range(mid, len(self.genes)))
        return DNA(new_genes)

    def mutate(self):
        mutation_rate = 0.01
        for i in range(len(self.genes)):
            if random.random() < mutation_rate:
                a, b = (math.Vector2(random.randint(-1, 1), random.randint(-1, 1)))

                # change magnitude of the vector to 0.1
                a *= 0.1
                b *= 0.1
                self.genes[i] = (a, b)
