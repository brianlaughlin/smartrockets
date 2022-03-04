"""
Smart Rocket Simulation using generic algorithm
Rocket will have physics using vectors
Program will use Pygame to simulate the rockets
We'll have DNA and come mutation and cross over
Program will have a population and the fitness function will evaluate how close the rocket is to the target

Taken from https://www.youtube.com/watch?v=bGz7mv2vD6g
"""

import pygame
import random
import constants
from moon import Moon

from rocket import Rocket

pygame.init()

# initialize for fonts
pygame.font.init()

LIFE_FONT = pygame.font.SysFont("comicsansms", 10)
SUCCESS_FONT = pygame.font.SysFont("comicsansms", 10)

FPS = 60

pygame.display.set_caption("Smart Rocket Simulation")

WIN = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))



# Global Variables
life_counter = 0
success_counter = 0


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
            new_population.append(Rocket(constants.WHITE, child))

        self.rockets = new_population
        self.generation += 1

    def run(self):
        for i in range(self.pop_size):
            self.rockets[i].update(life_counter)
            self.rockets[i].show(WIN)


def draw(WIN, rocket_population, moon, obstacles_list):
    global life_counter
    global success_counter

    WIN.fill(constants.WHITE)

    life_text = LIFE_FONT.render(f"Count: {life_counter}", 1, constants.BLACK)
    WIN.blit(life_text, (10, 10))

    success_text = LIFE_FONT.render(f"Success: {success_counter}", 1, constants.BLACK)
    WIN.blit(success_text, (10, 30))

    moon.draw(WIN)

    # draw a black rectangle filled in black
    for obstacle in obstacles_list:
        pygame.draw.rect(WIN, constants.BLACK, (obstacle[0], obstacle[1], 10, 10))

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
        if rocket.pos.x > constants.WIDTH or rocket.pos.x < 0 or rocket.pos.y > constants.HEIGHT or rocket.pos.y < 0:
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
        if life_counter >= constants.LIFESPAN:
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
