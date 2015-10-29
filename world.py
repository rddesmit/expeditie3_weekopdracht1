import csv
import pygame

class World:


    def __init__(self):
        # laad de kaart
        [lines, MIN_X, MAX_X, MIN_Y, MAX_Y] = self.load_map("assets/testmaze.txt")
        self.lines = lines
        self.MIN_X = MIN_X
        self.MAX_X = MAX_X
        self.MIN_Y = MIN_Y
        self.MAX_Y = MAX_Y
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.BORDER = 10
        self.SCALE_X = float(self.SCREEN_WIDTH - 2*self.BORDER) / (MAX_X - MIN_X)
        self.SCALE_Y = float(self.SCREEN_HEIGHT - 2*self.BORDER) / (MAX_Y - MIN_Y)

        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def load_map(self, filename):
        """
        Laadt de wereld in uit een tekstbestand.
        De wereld bestaat uit rechte muren (lijnen) waarvan je de x en
        y coordinaten van de uiteinden in meters(!) spatiegescheiden in dit
        bestand zet
        x1 y1 x2 y2
        is dus een muur van x1, y1 naar x2, y2
        """
        lines = []

        min_x = 1000000
        min_y = 1000000
        max_x = -1000000
        max_y = -1000000

        with open(filename) as tsv:
            for row in csv.reader(tsv, delimiter=" "):
                x1 = float(row[0])
                y1 = float(row[1])
                x2 = float(row[2])
                y2 = float(row[3])

                line = [x1, y1, x2, y2]

                min_x = min(x1, x2, min_x)
                max_x = max(x1, x2, max_x)
                min_y = min(y1, y2, min_y)
                max_y = max(y1, y2, max_y)

                lines.append(line)

        return [lines, min_x, max_x, min_y, max_y]

    def scale_point(self, x, y):
        return int(self.SCALE_X * (x - self.MIN_X) + self.BORDER), int(self.SCALE_Y * (y - self.MIN_Y) + self.BORDER)

    def draw_lines(self, screen, lines):
        for line in lines:
            pygame.draw.line(screen, (0, 0, 0), self.scale_point(line[0], line[1]), self.scale_point(line[2], line[3]), 5)

    def draw_particles(self, screen, particles):
        for particle in particles:
            (x, y) = self.scale_point(particle.x, particle.y)
            pygame.draw.rect(screen, (255, 0, 0), (x, y, 3, 3), 0)