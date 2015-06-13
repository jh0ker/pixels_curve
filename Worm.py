#!/usr/bin/python
__author__ = 'Jannes Hoeke'

from Colors import *
import random
from Powerup import Powerup

# A Worm
class Worm(pygame.sprite.OrderedUpdates):

    UP, RIGHT, DOWN, LEFT = range(4)

    def __init__(self, position, color, player):
        pygame.sprite.OrderedUpdates.__init__(self)

        self.position = position
        self.thickness = 1
        self.color = color

        if player == 1 or player == 3:
            self.direction = self.RIGHT
        else:
            self.direction = self.LEFT

        self.player = player
        self.gap = 0
        self.lastgap = 0

        self._rand = random.Random()
        self.lastpos = position
        self.powerups = {}

        self.turned = False

    def move(self):
        thick = Powerup.THICK in self.powerups
        speed = Powerup.SPEED in self.powerups
        slow = Powerup.SLOW in self.powerups
        invis = Powerup.INVISIBLE in self.powerups

        self.thickness = 2 if thick and not invis else 1

        self.lastpos = self.position

        if self.direction == self.UP:
            self.position = (self.position[0] - (1 if self.turned == self.LEFT and self.thickness > 1 else 0), self.position[1] - 1)
        elif self.direction == self.DOWN:
            self.position = (self.position[0] - (1 if self.turned == self.RIGHT and self.thickness > 1 else 0), self.position[1] + (2 if not self.turned == -1 and self.thickness > 1 else 1))
        elif self.direction == self.LEFT:
            self.position = (self.position[0] - 1, self.position[1] - (1 if self.turned == self.RIGHT and self.thickness > 1 else 0))
        elif self.direction == self.RIGHT:
            self.position = (self.position[0] + (2 if not self.turned == -1 and self.thickness > 1 else 1), self.position[1])

        self.lastgap = self.gap

        if self.is_gap():
            self.gap -= self.thickness

        if not self.was_gap() and self._rand.random() < 0.09:
            self.gap = self._rand.randint(3, 5)

        for k in self.powerups.keys():
            self.powerups[k] -= 1
            if self.powerups[k] == 0:
                del self.powerups[k]

        self.turned = -1
        return Head(self.position, self.color, (1, self.thickness)) if self.direction == self.RIGHT or self.direction == self.LEFT else Head(self.position, self.color, (self.thickness, 1))

    def turn(self, direction):

        if Powerup.REVERSE in self.powerups:
            direction = self.RIGHT if direction == self.LEFT else self.RIGHT

        self.turned = direction
        if direction == self.RIGHT:
            self.direction = (self.direction + 1) % 4
        elif direction == self.LEFT:
            self.direction = (self.direction - 1 + 4) % 4

    def is_gap(self):
        return self.gap >= 0

    def was_gap(self):
        return self.lastgap >= 0


class Head(pygame.sprite.Sprite):

    def __init__(self, position, color, size = (1, 1)):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = position