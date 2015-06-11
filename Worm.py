#!/usr/bin/python
__author__ = 'Jannes Hoeke'

from Colors import *

# A Worm
class Worm(pygame.sprite.OrderedUpdates):

    UP, RIGHT, DOWN, LEFT = range(4)

    def __init__(self, position, color, player):
        pygame.sprite.OrderedUpdates.__init__(self)

        self.position = position
        self.color = color
        self.direction = self.DOWN
        self.player = player

    def move(self):

        if self.direction == self.UP:
            self.position = (self.position[0], self.position[1] - 1)
        elif self.direction == self.LEFT:
            self.position = (self.position[0] - 1, self.position[1])
        elif self.direction == self.RIGHT:
            self.position = (self.position[0] + 1, self.position[1])
        elif self.direction == self.DOWN:
            self.position = (self.position[0], self.position[1] + 1)

        return Head(self.position, self.color)

    def turn(self, direction):
        if direction == self.RIGHT:
            self.direction = (self.direction + 1) % 4
        elif direction == self.LEFT:
            self.direction = (self.direction - 1 + 4) % 4

class Head(pygame.sprite.Sprite):

    def __init__(self, position, color):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((1, 1))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = position