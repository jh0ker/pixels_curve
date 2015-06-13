#!/usr/bin/python
__author__ = 'Jannes Hoeke'

import led
import sys
from Colors import *
from led.PixelEventHandler import *
from Worm import Worm

""" https://github.com/jh0ker/pixels_curve
    based on https://github.com/HackerspaceBremen/pixels_basegame
    depends on https://github.com/HackerspaceBremen/pygame-ledpixels
"""

MENU, GAME = range(2)

class Curve:

    def __init__(self):
        self.clock = pygame.time.Clock()
        pygame.joystick.init()

        # Initialize first joystick
        if pygame.joystick.get_count() > 0:
            stick = pygame.joystick.Joystick(0)
            stick.init()

        fallback_size = (90, 20)

        self.ledDisplay = led.dsclient.DisplayServerClientDisplay('localhost', 8123, fallback_size)

        pygame.font.init()
        self.font_text = pygame.font.SysFont(None, 18)

        # use same size for sim and real LED panel
        size = self.ledDisplay.size()
        self.simDisplay = led.sim.SimDisplay(size)
        self.screen = pygame.Surface(size)

        self.ticks = 0
        self.fps = 5
        self.gameover = False
        self.winner = None

        self.players = 2
        self.worms = []
        self.surfaces = []
        self.dead_worms = []
        self.state = MENU

    # Draws the surface onto the display(s)
    def update_screen(self, surface):
        self.simDisplay.update(surface)
        self.ledDisplay.update(surface)

    # Gameloop update
    def update(self):
        screen = self.screen

        # Count ticks independently of time so the timings won't mess up if the CPU is slow (you don't HAVE to use this,
        # but I recommend it, since I had problems with this
        self.ticks += 1
        ticks = self.ticks

        # Example
        if self.state == MENU:
            write_worms = self.font_text.render("Players: " + str(self.players), True, WHITE)

            screen.fill(BLACK)
            screen.blit(write_worms, (2, 4))

        elif self.state == GAME:
            p = range(self.players)
            for i in p:
                w = self.worms[i]

                head = w.move()

                dead = False
                gap = w.is_gap()

                if head.rect.x < 0 or head.rect.x >= 90 or head.rect.y < 0 or head.rect.y >= 20:
                    self.worms.remove(w)
                    self.dead_worms.append(w)
                    self.players -= 1
                    p.pop()
                    dead = True

                if not dead and not gap:
                    for w2 in self.worms:
                        if not dead and pygame.sprite.spritecollideany(head, w2):
                            self.worms.remove(w)
                            self.dead_worms.append(w)
                            self.players -= 1
                            p.pop()
                            dead = True

                if not dead and not gap:
                    for w2 in self.dead_worms:
                        if not dead and pygame.sprite.spritecollideany(head, w2):
                            self.worms.remove(w)
                            self.dead_worms.append(w)
                            self.players -= 1
                            p.pop()
                            dead = True

                if not dead:
                    self.screen.blit(head.image, head.rect)

                    if w.was_gap() and screen.get_at(w.lastpos) == w.color:  # Not perfect, erases own old lines
                        coverup = pygame.Surface((1, 1))
                        coverup.fill(BLACK)
                        self.screen.blit(coverup, w.lastpos)

                    if not gap:
                        w.add(head)

                elif self.players == 1:
                    self.gameover = True
                    self.winner = self.worms[0].player
                    break

        # Print fps
        if ticks % self.fps == 0:
            print self.clock.get_fps()

    def main(self):

        screen = self.screen

        # Show loading message
        font_text = self.font_text

        write_lobby = font_text.render("Basegame", True, WHITE)

        screen.fill(BLACK)
        screen.blit(write_lobby, (2, 4))

        self.update_screen(screen)

        # Clear event list before starting the game
        pygame.event.clear()

        while not self.gameover:

            # Process event queue
            for pgevent in pygame.event.get():
                if pgevent.type == QUIT:
                    pygame.quit()
                    sys.exit()

                event = process_event(pgevent)

                # End the game
                if event.button == EXIT:
                    self.gameover = True

                elif event.type == PUSH and self.state == MENU:
                    if event.button == UP and self.players < 4:
                        self.players += 1
                    elif event.button == DOWN and self.players > 2:
                        self.players -= 1
                    elif event.button == B1:
                        for i in range(self.players):
                            if i == 0:
                                self.worms.append(Worm((9, 4), RED, 1))
                            elif i == 1:
                                self.worms.append(Worm((79, 4), BLUE, 2))
                            elif i == 2:
                                self.worms.append(Worm((9, 14), YELLOW, 3))
                            elif i == 3:
                                self.worms.append(Worm((79, 14), WHITE, 4))

                            s = pygame.Surface(self.ledDisplay.size())
                            s.set_colorkey(BLACK)
                            s.fill(BLACK)
                            self.surfaces.append(s)

                        screen.fill(BLACK)

                        self.state = GAME

                # Keypresses on keyboard and joystick axis motions / button presses
                elif event.type == PUSH and self.state == GAME:
                    if event.player == PLAYER1:
                        # Joysticks
                        if event.button == LEFT and self.players >= 1:
                            self.worms[0].turn(Worm.LEFT)
                        elif event.button == RIGHT and self.players >= 1:
                            self.worms[0].turn(Worm.RIGHT)

                        # Buttons
                        elif event.button == B1 and self.players >= 3:
                            self.worms[2].turn(Worm.LEFT)
                        elif event.button == B2 and self.players >= 3:
                            self.worms[2].turn(Worm.RIGHT)

                    # Same stuff here
                    elif event.player == PLAYER2:
                                                # Joysticks
                        if event.button == LEFT and self.players >= 2:
                            self.worms[1].turn(Worm.LEFT)
                        elif event.button == RIGHT and self.players >= 2:
                            self.worms[1].turn(Worm.RIGHT)

                        # Buttons
                        elif event.button == B1 and self.players >= 4:
                            self.worms[3].turn(Worm.LEFT)
                        elif event.button == B2 and self.players >= 4:
                            self.worms[3].turn(Worm.RIGHT)

            ''' Draw stuff here
            '''

            self.update()

            '''
            '''

            # Update screen
            self.update_screen(screen)

            # Tick the clock and pass the maximum fps
            self.clock.tick(self.fps)

        # End of the game
        write_gameover = font_text.render("GAME OVER", True, WHITE)

        screen.blit(write_gameover, (10, 4))

        self.update_screen(screen)

        # Wait for keypress
        while True:
            event = process_event(pygame.event.wait())
            if event.type == PUSH:
                break

        # Show score
        text_gameover = "Winner: " + str(self.winner)
        write_gameover = font_text.render(text_gameover, True, WHITE)

        screen.fill(BLACK)
        screen.blit(write_gameover, (2, 4))

        self.update_screen(screen)

        # Wait for keypress
        while True:
            event = process_event(pygame.event.wait())
            if event.type == PUSH:
                break

        pygame.quit()
    
game = Curve()
game.main()
