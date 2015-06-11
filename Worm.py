#!/usr/bin/python
__author__ = 'Jannes Hoeke'

from Colors import *
import random

# A Worm
class Worm(pygame.sprite.OrderedUpdates):

    UP, RIGHT, DOWN, LEFT = range(4)

    def __init__(self, position, color, player):
        pygame.sprite.OrderedUpdates.__init__(self)

        self.position = position
        self.color = color
        if player == 1 or player == 2:
            self.direction = self.DOWN
        else:
            self.direction = self.UP
        self.player = player

        self.gap = 0
        self.lastgap = 0

        self._rand = random.Random()

        self.lastpos = position

    def move(self):

        self.lastpos = self.position

        if self.direction == self.UP:
            self.position = (self.position[0], self.position[1] - 1)
        elif self.direction == self.LEFT:
            self.position = (self.position[0] - 1, self.position[1])
        elif self.direction == self.RIGHT:
            self.position = (self.position[0] + 1, self.position[1])
        elif self.direction == self.DOWN:
            self.position = (self.position[0], self.position[1] + 1)

        if self.gap == 0 and self._rand.random() < 0.1:
            self.gap = self._rand.randint(3, 5)

        self.lastgap = self.gap

        if not self.gap == 0:
            self.gap -= 1

        return Head(self.position, self.color)

    def turn(self, direction):
        if direction == self.RIGHT:
            self.direction = (self.direction + 1) % 4
        elif direction == self.LEFT:
            self.direction = (self.direction - 1 + 4) % 4

    def is_gap(self):
        return not self.gap == 0

    def was_gap(self):
        return not self.lastgap == 0


class Head(pygame.sprite.Sprite):

    def __init__(self, position, color):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((1, 1))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = position