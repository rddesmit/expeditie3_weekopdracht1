# Markov class

from orientation import Orientation

class Markov:
    """
    Class voor Markov Localisatie (histogram filter)

    Dit is het belangrijkste deel van de opdracht

    """

    def __init__(self, world, orientation, name, p_hit=.7, p_overshoot=.1, p_undershoot=.1):
        """
        Geef Markov de kaart, initiele robot orientatie en een naam voor deze Markov
        """

        def initUniformDistribution():
            ylength = len(world)
            xlength = len(world[0])

            p = 1. / (ylength * xlength)

            return [[p for x in y] for y in world]

        # !!! Coordinates are swapped, because multidimensional arrays are used !!!
        # (x,y) => map[y][x]
        # orientations are swapped accordingly
        # set world and orientatio
        self._world = world
        self._orientation = orientation
        self._name = name

        # TODO: initialiseer de Markov (uniform distribution)
        self._p = initUniformDistribution()

        # TODO: pas deze waarden aan om de robot meer of minder accuraat te maken
        # init sensor probabilities
        self._pHit = p_hit
        self._pMiss = 1. - self._pHit
        self._pOvershoot = p_overshoot
        self._pUndershoot = p_undershoot
        self._pExact = 1. - self._pOvershoot - self._pUndershoot

    def normalize(self):
        """
        Normaliseer de Markov
        """

        # TODO: Normaliseer de distribution
        total = reduce(lambda acc, c: acc + sum(c), self._p, 0.)
        self._p = [[x / total for x in y] for y in self._p]

    def __str__(self):
        """
        String representatie van de Markov
        """

        debug_string = "World #" + self._name + "\nOrientation: " + str(self._orientation) + "\n"
        debug_string = "\n" + debug_string + "Best estimate: " + str(self.current_estimate()) + "\n\n"

        return debug_string

    def rotate_left(self):
        self.rotate(-1)

    def rotate_right(self):
        self.rotate(1)

    def rotate(self, direction):
        """
        Draai de orientatie

        -1 = left, +1 = right
        """

        # TODO: Zorg dat je begrijpt waarom dit werkt
        self._orientation = (self._orientation + direction) % 4

    def update(self, measurement):
        """
        Update de kansen in de Markov (measurement)
        """

        def calculate(color, xi, yi):
            p = self._p[yi][xi]
            p = p * self._pHit if color == measurement else p * self._pMiss
            self._p[yi][xi] = p

        # TODO: Update de Markov nadat er een bepaalde waarneming (de measurement) gedaan is
        [[calculate(x, xi, yi) for (xi, x) in enumerate(y)] for (yi, y) in enumerate(self._world)]
        self.normalize()

    def move(self, distance=1):
        """
        Verplaats de kansen in de Markov (convolution)
        """

        def move_north(d):
            def p(yi, xi):
                s = self._pExact * self._p[(yi+d) % len(self._p)][xi]
                s += self._pOvershoot * self._p[(yi+d-1) % len(self._p)][xi]
                s += self._pUndershoot * self._p[(yi+d+1) % len(self._p)][xi]
                return s

            self._p = [[p(yi, xi) for (xi, x) in enumerate(y)] for (yi, y) in enumerate(self._p)]

        def move_east(d):
            def p(yi, xi):
                s = self._pExact * self._p[yi][(xi-d) % len(self._p[0])]
                s += self._pOvershoot * self._p[yi][(xi-d-1) % len(self._p[0])]
                s += self._pUndershoot * self._p[yi][(xi-d+1) % len(self._p[0])]
                return s

            self._p = [[p(yi, xi) for (xi, x) in enumerate(y)] for (yi, y) in enumerate(self._p)]

        def move_south(d):
            move_north(d * -1)

        def move_west(d):
            move_east(d * -1)

        # TODO: Update de Markov nadat er een beweging gedaan is (de convolution)
        if self._orientation == Orientation.NORTH:
            move_north(distance)
        elif self._orientation == Orientation.EAST:
            move_east(distance)
        elif self._orientation == Orientation.SOUTH:
            move_south(distance)
        elif self._orientation == Orientation.WEST:
            move_west(distance)

        self.normalize()

    def current_estimates(self):
        """
        Geef alle kansen terug gesorteerd op waarschijnlijkheid (beste esitimate eerst)
        """

        # TODO: zet alle esimates in een lijst met tuples (kans, row, column)
        estimates = [(x, yi, xi) for (yi, y) in enumerate(self._p) for (xi, x) in enumerate(y)]
        estimates.sort()
        estimates.reverse()

        return estimates

    def current_estimate(self):
        """
        Geef de beste estimate
        """
        estimates = self.current_estimates()

        if len(estimates) > 0:
            return estimates[0]
        else:
            return None
