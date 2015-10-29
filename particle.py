import random
import math

"""
De Particle class is gebaseerd op de Robot-class van Udacity, maar omdat ik Robot al voor de EV3 gebruik
heb ik hem een andere naam gegeven.
"""


class Particle:
    """
    Een particle met instelbare bewegings- en sensorruis
    """
    def __init__(self, world, sensordirections):
        """
        Kiest zelf een willekeurige plek. Geef bij init de richtingen van de sensors mee (0 is recht vooruit)
        """
        self.world = world
        self.x = random.random() * (self.world.MAX_X - self.world.MIN_X) + self.world.MIN_X
        self.y = random.random() * (self.world.MAX_Y - self.world.MIN_Y) + self.world.MIN_Y
        self.orientation = random.random() * 2.0 * math.pi
        self.forward_noise = 0.0
        self.turn_noise = 0.0
        self.sense_noise = 0.0

        self._sensordirections = sensordirections

    def _set(self, new_x, new_y, new_orientation):
        if new_x < self.world.MIN_X or new_x > self.world.MAX_X:
            raise ValueError, 'X coordinate out of bound'
        if new_y < self.world.MIN_Y or new_y > self.world.MAX_Y:
            raise ValueError, 'Y coordinate out of bound'
        if new_orientation < 0 or new_orientation >= 2 * math.pi:
            raise ValueError, 'Orientation must be in [0..2pi]'
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)

    def set_noise(self, new_f_noise, new_t_noise, new_s_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.forward_noise = float(new_f_noise)
        self.turn_noise = float(new_t_noise)
        self.sense_noise = float(new_s_noise)

    def _sense(self, screen, draw=False): # zou met lines moeten gaan werken ipv screen

        # kleur van de muren (voor detectie)
        DETECTIONCOLOR = (0, 0, 0, 255)

        # de kanten waarheen de sensoren kijken
        DIRECTIONS = self._sensordirections

        # minder nauwkeurig dan netjes met 1 stap, maar kan wel verder kijken zonder dat het
        # extra rekenkracht kost
        SENSORSTEP = 0.01

        # aantal stappen dat vooruit gekeken wordt
        SENSORDISTANCE = 100.

        # array om alle sensorafstanden in op te slaan
        dist = []

        for i in range(len(DIRECTIONS)):

            # tijdelijke variabelen: startpunt, eindclausule, afstand en richting van de sensor
            tempX = self.x
            tempY = self.y
            detected = False
            distance = 0
            dX = (math.cos(self.orientation + DIRECTIONS[i]) * SENSORSTEP)
            dY = (math.sin(self.orientation + DIRECTIONS[i]) * SENSORSTEP)

            # zolang nog in de wereld, binnen bereik van de sensor en niet gedetecteerd zoeken naar een muur
            while (tempX > self.world.MIN_X) and (tempY > self.world.MIN_Y) and (tempX < self.world.MAX_X) and (tempY < self.world.MAX_Y) and not detected and (distance < SENSORDISTANCE):
                # volgende stap
                distance = distance + 1
                tempX = tempX + dX
                tempY = tempY + dY

                detectedColor = screen.get_at(self.world.scale_point(tempX, tempY))

                # optioneel tekenen van de sensor
                if draw:
                    screen.set_at(self.world.scale_point(tempX, tempY), (255,0,0,255))

                if detectedColor == DETECTIONCOLOR:
                    detected = True

            dist.append(distance)

        return dist

    def move(self, turn, forward):
        """
        Geef het particle een beweging en draai mee.

        LET OP!!! Het particle-object zelf wordt niet bewogen. Er wordt een nieuw object
                    gecreeerd dat op de nieuwe positie staat en gereturnd

        """
        if forward < 0:
            raise ValueError, 'Robot cant move backwards'

        # turn, and add randomness to the turning command
        orientation = self.orientation + float(turn) + random.gauss(0.0, self.turn_noise)
        orientation %= 2 * math.pi

        # move, and add randomness to the motion command
        dist = float(forward) + random.gauss(0.0, self.forward_noise)
        x = self.x + (math.cos(orientation) * dist)
        y = self.y + (math.sin(orientation) * dist)

        if x > self.world.MAX_X:
            x = self.world.MIN_X
        if y > self.world.MAX_Y:
            y = self.world.MAX_Y
        if x < self.world.MIN_X:
            x = self.world.MAX_X
        if y < self.world.MIN_Y:
            y = self.world.MAX_Y

        # set particle
        res = Particle(self.world, self._sensordirections)
        res._set(x, y, orientation)
        res.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        return res

    def Gaussian(self, mu, sigma, x):
        # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        return math.exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / math.sqrt(2.0 * math.pi * (sigma ** 2))

    def measurement_prob(self, measurement, screen):
        compare = self._sense(screen)
        return reduce(lambda acc, (m, c): acc / math.fabs(m - c) if m != c else acc, zip(measurement, compare), 1.)


    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))