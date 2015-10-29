import math
import pygame
from particle import Particle


class ParticleFilterSimulatedRobot:
    def __init__(self, world, sensordirections, x, y, orientation):
        self._robot = Particle(world, sensordirections)
        self._robot._set(x, y, orientation)
        self._robot.set_noise(0., 0., 0.) # TODO: use realistic values
        self._world = world
        self._image = pygame.image.load("assets/robot.png").convert_alpha()

    def connect_ultrasone(self, ports=['in2:i2c1'], offsets=[0]):
        pass

    def connect_ir(self, ports=['in1'], offsets=[0]):
        pass

    def turn(self, rad):
        # calc ticks
        self._robot = self._robot.move(rad, 0)
        self.draw()

    def turn_right(self, rad=0.5*math.pi):
        self.turn(rad)

    def turn_left(self, rad=0.5*math.pi):
        self.turn(-rad)

    def drive(self, dist=0.10):
        self._robot = self._robot.move(0, dist)
        self.draw()

    def sense_ultrasone(self):
        return self._robot._sense(self._world.screen, True)

    def sense_ir(self):
        return self._robot._sense(self._world.screen)

    def draw(self):
        rot_image = pygame.transform.rotate(self._image, float(-self._robot.orientation - (0.5*math.pi)) / (2.*math.pi) * 360)

        [x, y] = self._world.scale_point(self._robot.x,self._robot.y)
        self._world.screen.blit(rot_image, (x-25, y-22))