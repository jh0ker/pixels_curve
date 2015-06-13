__author__ = 'Jannes Hoeke'

from Colors import *

# The cursor to place towers and to select towers
class Powerup(pygame.sprite.Sprite):

    SPEED, SLOW, REVERSE, INVISIBLE, THICK = range(5)

    def __init__(self, type, position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()

        if type == self.SPEED:
            self.image.fill(GREEN)
        elif type == self.SLOW:
            self.image.fill(RED)
        elif type == self.REVERSE:
            self.image.fill(MAGENTA)
        elif type == self.INVISIBLE:
            self.image.fill(BLUE)
        elif type == self.THICK:
            self.image.fill(CYAN)

        self.rect.topleft = position

        self.type = type
