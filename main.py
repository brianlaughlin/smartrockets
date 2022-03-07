"""
Smart Rocket Simulation using generic algorithm
Rocket will have physics using vectors
Program will use Pygame to simulate the rockets
We'll have DNA and come mutation and cross over
Program will have a population and the fitness function will evaluate how close the rocket is to the target

Taken from https://www.youtube.com/watch?v=bGz7mv2vD6g
"""

import pygame
import constants
from moon import Moon
from population import population

pygame.init()

# initialize for fonts
pygame.font.init()

DEFAULT_FONT = pygame.font.SysFont("comicsansms", 10)

pygame.display.set_caption("Smart Rocket Simulation")

WIN = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))

# Global Variables
life_counter = 0
success_counter = 0
success_count_highest = 0
number_of_generations = 0


def draw(WIN, rocket_population, moon, obstacles_list):
    global life_counter
    global success_counter
    global success_count_highest
    global number_of_generations

    WIN.fill(constants.WHITE)

    life_text = DEFAULT_FONT.render(f"Count: {life_counter}", True, constants.BLACK)
    WIN.blit(life_text, (10, 10))

    success_text = DEFAULT_FONT.render(f"Success: {success_counter}", True, constants.BLACK)
    WIN.blit(success_text, (10, 30))

    success_count_highest_text = DEFAULT_FONT.render(f"Highest: {success_count_highest}", True, constants.BLACK)
    # place to the right of success text and account for the width of the text
    WIN.blit(success_count_highest_text, (success_text.get_width() + 16, 30))

    # add generation text called number_of_generations
    generation_text = DEFAULT_FONT.render(f"Generation: {number_of_generations}", True, constants.BLACK)
    WIN.blit(generation_text, (10, 50))

    right_click_text = DEFAULT_FONT.render("Right Click Move Moon", True, constants.BLUE)
    # display in bottom right corner, calculate position using constants and place above start_over_text
    WIN.blit(right_click_text, (constants.WIDTH - right_click_text.get_width() - 10,
                                constants.HEIGHT - right_click_text.get_height() - 30))

    start_over_text = DEFAULT_FONT.render("Press 's' to restart", True, constants.BLUE)
    # display in bottom right corner, calculate position using constants
    WIN.blit(start_over_text, (constants.WIDTH - start_over_text.get_width() - 10,
                               constants.HEIGHT - start_over_text.get_height() - 10))

    moon.draw(WIN)

    # draw a black rectangle filled in black
    for obstacle in obstacles_list:
        pygame.draw.rect(WIN, constants.BLACK, (obstacle[0], obstacle[1], 10, 10))

    rocket_population.run(WIN, life_counter)

    pygame.display.update()


def handle_collisions(rocket_population, moon, obstacles_list):
    global success_counter
    global success_count_highest

    for rocket in rocket_population.rockets:
        # check if rocket is colliding with moon rectangle
        if moon.x < rocket.pos.x < moon.x + moon.width and \
                rocket.pos.y > moon.y and rocket.pos.y < moon.y + moon.height:
            rocket.crashed = True
            rocket.success = True
            rocket.life_span_count = life_counter  # will use this for fitness function
            print(f"Rocket lifespan: {rocket.life_span_count}")

            # set rocket position to moon position to give best fitness score possible
            rocket.pos.x, rocket.pos.y = moon.x, moon.y
            rocket.visible = False

            success_counter += 1

            if success_count_highest < success_counter:
                success_count_highest = success_counter

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
    global success_count_highest
    global number_of_generations

    run = True
    clock = pygame.time.Clock()

    moon = Moon()
    drawing = False

    rocket_population_max = 100
    rocket_population = population(rocket_population_max)

    obstacle_list = []

    while run:
        clock.tick(constants.FPS)
        life_counter += 1
        if life_counter >= constants.LIFESPAN:
            life_counter = 0
            success_counter = 0
            number_of_generations += 1

            rocket_population.evaluate(moon)
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

            left, middle, right = pygame.mouse.get_pressed()
            # move the moon to the mouse position with right click
            if right:
                moon.move = True
                moon.x, moon.y = pygame.mouse.get_pos()
                print(moon.x, moon.y)

            # if 'S' is pressed redo population as new generation
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    rocket_population = population(rocket_population_max)
                    number_of_generations = 0

        handle_collisions(rocket_population, moon, obstacle_list)

        draw(WIN, rocket_population, moon, obstacle_list)

    pygame.quit()


if __name__ == '__main__':
    main()
