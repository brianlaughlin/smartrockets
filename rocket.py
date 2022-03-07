import math as m

import pygame
from pygame import math as math
from dna import DNA
import constants


class Rocket:
    def __init__(self, color, dna=None):
        self.x = constants.WIDTH / 2
        self.y = constants.HEIGHT - 50
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

    def update(self, life_counter):
        """
        Simple physics engine update
        """

        self.apply_force(self.dna.genes[life_counter])

        # if the rocket is not crashed
        if not self.crashed:
            self.vel += self.acc
            self.pos += self.vel
            self.acc *= 0

    def show(self, WIN):
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

    # todo: Improve fitness function
    # https://gamedev.stackexchange.com/questions/134732/genetic-algorithms-fitness-function-simple-maze-game?newreg=f8ccba1680b2402ea60385e33717ab6e
    def calculate_fitness(self, moon):
        """
        The closer the rocket is to the moon the more fit the rocket is.
        """

        # get distance from moon
        distance = m.sqrt((self.pos.x - moon.x) ** 2 + (self.pos.y - moon.y) ** 2)
        # get the distance from the moon and make sure to check for divide by 0
        if distance == 0:
            distance = 1
        self.fitness = 10 / distance if self.success else 1 / distance  # fitness is the inverse of distance

# todo: write using lifespan with distance. Improve fitness function by using time.
