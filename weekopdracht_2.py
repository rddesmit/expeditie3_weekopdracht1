"""

Monte Carlo Lokalisatie / Particle Filter

Dit is weekopdracht 2 voor expeditie 3, autonome voertuigen

Je bestuurt zelf je robot, maar mag niet kijken waar hij is. Gebruik een particle filter te ontdekken waar hij
is op de kaart van het doolhof waar hij ingezet is, en rijd dan naar de uitgang.

Je kunt de software eerst ontwikkelen met een gesimuleerde robot, en daarna uit laten voeren door de
EV3 met een differential drive en een drie afstandssensoren (links, voor en rechts).

Hoe je te werk gaat:

* Zorg dat je de theorie van Les 3 op Udacity goed begrijpt

* Lees de python bestanden door zodat je weet waar je alles kunt vinden

* Maak daarna het Particle filter werkend
    * Concentreer je eerst op de move,
    * en daarna op de measurement (resampling)

Bestanden:

* particle_weekopdracht_pygame.py: dit bestand, waarin je het filter programmeert
* robot.py: deze heb je pas nodig als je de EV3 gebruikt
* particle.txt: een testkaart. het formaat staat uitgelegd in de functie load_map als je zelf ook kaarten wil maken

NB.
In dit bestand vind je TODO's op de plaatsen waar je aanpassingen moet doen en aanwijzingen (in PyCharm kan je
die makkelijk vinden doordat ze blauw in de kantlijn staan)


"""

import csv
import pygame
import random
import math
from particle_robot import ParticleFilterSimulatedRobot
from world import World
from particle import Particle
from joblib import Parallel, delayed

SIMULATION = True
N_PARTICLES = 1000
SENSE_DIRECTIONS = [-0.5*math.pi, 0., 0.5*math.pi]

if not SIMULATION:
    from robot import Robot


def resample(particles, probabilities):
    """

    :param particles: een lijst met alle particles
    :param probabilities: een lijst een de samplewaarschijnlijkheid per particles in dezelfde volgorde
    :return: een geresamplede lijst met particles
    """

    # elke particle moet een 'grabbelkans' hebben
    assert (len(particles) == len(probabilities))

    # resample particles m.b.v. resampling wheel van Sebastian Thrun (lesson 3, Udacity: Artificial Intelligence for Robotics)

    # bepaal beginpunt op het wheel
    index = int(random.random()* len(probabilities))

    new_particles = []
    # bepaal grootste kans (vak op het wheel) en verdubbel deze als maximale draaiafstand, zodat je zelfs de
    # grootste kans kan missen
    max_distance = max(probabilities) * 2

    for i in range(len(particles)):
        B = random.random() * max_distance
        while (B > probabilities[index]):
            B = B - probabilities[index]
            index = (index + 1) % len(probabilities)

        new_particles.append(particles[index])
    return new_particles


def create_robot():
    return Robot if not SIMULATION else ParticleFilterSimulatedRobot(world, [-0.5*math.pi, 0., 0.5*math.pi], 2.40, 0.75, 0.5*math.pi)


def create_particles(world):
    particles = [Particle(world, SENSE_DIRECTIONS) for _ in range(N_PARTICLES)]
    for p in particles:
        p.set_noise(.1, .1, .1)
    return particles


world = World()
robot = create_robot()
particles = create_particles(world)

# verbind met de sensoren van de robot
robot.connect_ultrasone(['in1:i2c1', 'in2:i2c1', 'in3:i2c1'], [7.5,9.,10.])

# Fill background
background = pygame.Surface(world.screen.get_size())
background = background.convert()
background.fill((255, 255, 255))

# Blit everything to the screen
world.screen.blit(background, (0, 0))
pygame.display.flip()

running = 1

world.screen.fill((255, 255, 255))
world.draw_lines(world.screen, world.lines)
world.draw_particles(world.screen, particles)

# de robot kunnen we natuurlijk alleen tekenen bij simulatie
if SIMULATION:
    robot.draw()

# Teken de 'parkeerplaats'
pygame.draw.circle(world.screen, (255, 255, 0), world.scale_point(0.10, 0.10), 15)
pygame.display.flip()


# zolang het programma runt is de robot te besturen via de pijltjes
while running:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = 0

    # Teken de 'parkeerplaats'
    world.screen.fill((255, 255, 255))
    pygame.draw.circle(world.screen, (255, 255, 0), world.scale_point(0.10, 0.10), 15)
    world.draw_lines(world.screen, world.lines)

    if event.type == pygame.KEYDOWN:
        # stop
        if event.key == pygame.K_ESCAPE or event.unicode == 'q':
            break

        # omhoog
        if event.key == pygame.K_UP:
            # move
            robot.drive(.05)
            particles = [particle.move(.0, .05) for particle in particles]

        # draai links
        if event.key == pygame.K_LEFT:
            rad = -(0.25*math.pi)
            robot.turn(rad)
            particles = [particle.move(rad, .0) for particle in particles]


        # draai rechts
        if event.key == pygame.K_RIGHT:
            rad = 0.25*math.pi
            robot.turn(rad)
            particles = [particle.move(rad, .0) for particle in particles]

        # measure and resample
        measurement = robot.sense_ultrasone()
        p = [particle.measurement_prob(measurement, world.screen) for particle in particles]
        particles = resample(particles, p)
        world.draw_particles(world.screen, particles)
        pygame.display.flip()