"""
Smart Rocket Simulation using generic algorithm
Rocket will have physics using vectors
Program will use Pygame to simulate the rockets
We'll have DNA and come mutation and cross over
Program will have a population and the fitness function will evaluate how close the rocket is to the target

Taken from https://www.youtube.com/watch?v=bGz7mv2vD6g
"""

import pygame
import pygame.math as math
import random
import math as m

pygame.init()

# initialize for fonts
pygame.font.init()

WIDTH, HEIGHT = 800, 800

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIFE_FONT = pygame.font.SysFont("comicsansms", 10)
SUCCESS_FONT = pygame.font.SysFont("comicsansms", 10)

FPS = 60

pygame.display.set_caption("Smart Rocket Simulation")

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

LIFESPAN = 300

MOON_X, MOON_Y = WIDTH / 2, 50

# Global Variables
life_counter = 0
success_counter = 0


class Moon():
    def __init__(self):
        self.x = MOON_X
        self.y = MOON_Y
        self.image = pygame.image.load("assets/moon.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.width = self.rect.width
        self.height = self.rect.height

    def draw(self):
        WIN.blit(self.image, (self.x, self.y))


# Rocket class
class Rocket():
    def __init__(self, color, dna=None):
        self.x = WIDTH / 2
        self.y = HEIGHT - 50
        self.pos = math.Vector2(self.x, self.y)
        self.dna = DNA() if dna is None else dna
        self.life_span_count = 0

        # randomize the velocity with it going up
        self.vel = math.Vector2(0, 0)
        self.acc = math.Vector2(0, 0)
        self.color = color
        self.thrust = False
        self.fitness = 0
        self.crashed = False
        self.success = False
        self.visible = True
        # load image in assets/3 rockets.png 3 images 100 px wide, take the 3rd image
        self.image = pygame.image.load("assets/rocket.png")
        # Shrink the width of image by 25%
        self.image = pygame.transform.scale(self.image,
                                            (int(self.image.get_width() * 0.25), int(self.image.get_height() * 0.25)))

    def apply_force(self, force):
        self.acc += force

    def update(self):
        """
        Simple physics engine update
        """
        global life_counter


        self.apply_force(self.dna.genes[life_counter])

        # if the rocket is not crashed
        if not self.crashed:
            self.vel += self.acc
            self.pos += self.vel
            self.acc *= 0


    def show(self):
        """
        Rotate image while keeping its center
        Point in the direction of the velocity
        """

        # solve for angle of velocity
        angle = m.atan2(self.vel.x, self.vel.y)
        degrees = m.degrees(angle) + 180  # so it's pointing in the right direction

        # rotate image
        rotate_image = pygame.transform.rotate(self.image, degrees)
        # get the center of the image
        center = rotate_image.get_rect().center
        # draw the image if visible
        if self.visible:
            WIN.blit(rotate_image, (self.pos.x - center[0], self.pos.y - center[1]))

    def calculate_fitness(self):
        """
        The closer the rocket is to the moon the more fit the rocket is.
        """
        # get distance from moon
        distance = m.sqrt((self.pos.x - MOON_X) ** 2 + (self.pos.y - MOON_Y) ** 2)
        # get the distance from the moon and make sure to check for divide by 0
        if distance == 0:
            distance = 1
        self.fitness = 10 / distance if self.success else 1 / distance # fitness is the inverse of distance


class DNA():
    def __init__(self, genes=None):
        if genes is None:
            self.genes = []

            for _ in range(LIFESPAN):
                # self.genes.append(math.Vector2(random.randint(-1, 1), random.randint(-1, 1)))
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


class population():
    def __init__(self, pop_size):
        self.rockets = []
        self.pop_size = pop_size
        self.mating_pool = []
        self.generation = 1

        self.rockets.extend(Rocket(WHITE) for _ in range(pop_size))

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
            self.mating_pool.extend(rocket for _ in range(n)) # add rocket to the mating pool n times


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
            new_population.append(Rocket(WHITE, child))

        self.rockets = new_population
        self.generation += 1

    def run(self):
        for i in range(self.pop_size):
            self.rockets[i].update()
            self.rockets[i].show()


def draw(WIN, rocket_population, moon, obstacles_list):
    global life_counter
    global success_counter

    WIN.fill(WHITE)

    life_text = LIFE_FONT.render(f"Count: {life_counter}", 1, BLACK)
    WIN.blit(life_text, (10, 10))

    success_text = LIFE_FONT.render(f"Success: {success_counter}", 1, BLACK)
    WIN.blit(success_text, (10, 30))

    moon.draw()

    # draw a black rectangle filled in black
    for obstacle in obstacles_list:
        pygame.draw.rect(WIN, BLACK, (obstacle[0], obstacle[1], 10, 10))

    rocket_population.run()

    pygame.display.update()


def handle_collisions(rocket_population, moon, obstacles_list):
    global success_counter

    for rocket in rocket_population.rockets:
        # check if rocket is colliding with moon rectangle
        if rocket.pos.x > moon.x and rocket.pos.x < moon.x + moon.width and \
                rocket.pos.y > moon.y and rocket.pos.y < moon.y + moon.height:
            rocket.crashed = True
            rocket.success = True
            # set rocket position to moon position to give best fitness score possible
            rocket.pos.x, rocket.pos.y = moon.x, moon.y
            rocket.visible = False

            success_counter += 1

        # stop rockets from going off screen
        if rocket.pos.x > WIDTH or rocket.pos.x < 0 or rocket.pos.y > HEIGHT or rocket.pos.y < 0:
            rocket.crashed = True

        # check if rocket is colliding with obstacles
        for obstacle in obstacles_list:
            if rocket.pos.x > obstacle[0] and rocket.pos.x < obstacle[0] + 10 and \
                rocket.pos.y > obstacle[1] and rocket.pos.y < obstacle[1] + 10:
                rocket.crashed = True



def main():
    global life_counter
    global success_counter

    run = True
    clock = pygame.time.Clock()

    moon = Moon()
    drawing = False

    rocket_population_max = 100
    rocket_population = population(rocket_population_max)

    obstacle_list = []

    while run:
        clock.tick(FPS)
        life_counter += 1
        if life_counter >= LIFESPAN:
            life_counter = 0
            success_counter = 0

            rocket_population.evaluate()
            rocket_population.selection()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


            # if mouse button is held and mouse is moving save position in obstacle list
            # do not save if mouse button is released
            if event.type == pygame.MOUSEMOTION:
                if event.buttons[0] == 1:
                    drawing = True
                    x, y = pygame.mouse.get_pos()
                    obstacle_list.append((x, y))
                elif event.type == pygame.MOUSEBUTTONUP:
                    drawing = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    drawing = True



        handle_collisions(rocket_population, moon, obstacle_list)

        draw(WIN, rocket_population, moon, obstacle_list)

    pygame.quit()


if __name__ == '__main__':
    main()
