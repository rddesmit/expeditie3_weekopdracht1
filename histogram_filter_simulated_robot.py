# HistogramFilterSimulatedRobot class voor testen


import pygame
import math
import random
from colors import Colors


class HistogramFilterSimulatedRobot:

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    """
    Deze class accepteert dezelfde commando's als de echte robot class, en kan dus gebruikt worden voor
    testen.
    Na elke beweging (turn of drive) wordt de simulatie getekend.

    NB. De simulatierobot kan alleen maar 1 vakje vooruit rijden, en 90 graden draaien.

    Deze class hoef je niet aan te passen, alleen de waarden voor OVERSHOOT, UNDERSHOOT en PHIT
    zou je mee kunnen experimeteren
    """

    def __init__(self, map, row, column, orientation):
        """
        geef pygame-screen, de kaart, en de initiele positie van de simu-robot mee
        """
        pygame.init()
        screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self._screen = screen
        self._map = map
        self._row = row
        self._column = column
        self._orientation = orientation
        self._orientations = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        self._image = pygame.image.load("assets/robot.png").convert_alpha()
        self._estimate = (1, 1, 1)  # belief, row, col

        # TODO: pas deze waarden aan om de gesimuleerde robot meer of minder accuraat te maken
        # De kans dat de gesimuleerde robot doorschiet, op zijn plaats blijft na een beweging
        self.OVERSHOOT = 0.05
        self.UNDERSHOOT = 0.05
        # De kans dat de gesimuleerde robot de kleur goed zien
        self.PHIT = 0.9

    def draw(self):
        """
        Teken de simulatie

        Alleen voor inter gebruik
        """
        self._screen.fill((255, 255, 255))

        row_size = self.SCREEN_HEIGHT / len(self._map)
        col_size = self.SCREEN_WIDTH / len(self._map[0])

        for i in range(len(self._map)):
            for j in range(len(self._map[0])):
                col = self._map[i][j]
                pygame.draw.rect(self._screen, Colors.COLOR_TO_RGB[col], (col_size * j, row_size * i, col_size, row_size), 0)

        # LET OP! Niet beveiligd tegen van de kaart afrijden
        rot_image = pygame.transform.rotate(self._image,
                                            float(-self._orientation * (0.5 * math.pi)) / (2. * math.pi) * 360)

        [y, x] = self._row * row_size + (row_size / 2), self._column * col_size + (col_size / 2)
        self._screen.blit(rot_image, (x - 25, y - 22))

        pygame.display.flip()

    def connect_color(self):
        pass

    def drive(self, dist=0.10):
        distance = 1  # Ook andere afstanden mogelijk maken?
        r = random.random()

        if r < self.UNDERSHOOT:
            distance = 0
        elif r > (1. - self.OVERSHOOT):
            distance = 2

        self._row = (distance * self._orientations[self._orientation][0] + self._row)
        self._column = (distance * self._orientations[self._orientation][1] + self._column)
        self.draw()

    def sense_color(self):
        if random.random() > self.PHIT:
            return Colors.UNKNOWN
        else:
            return self._map[self._row][self._column]

    def rotate(self, direction):
        self._orientation = (self._orientation + direction) % 4
        self.draw()

    def turn_right(self, rad=0.5 * math.pi):
        self.rotate(1)

    def turn_left(self, rad=0.5 * math.pi):
        self.rotate(-1)
