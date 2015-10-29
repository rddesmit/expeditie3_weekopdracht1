"""

Markov Lokalisatie / Histogram Filter

Dit is weekopdracht 1 voor expeditie 3, autonome voertuigen

Gebruik een histogram filter om een robot te laten ontdekken waar hij is op een kaart van gekleurde
vlakjes, en rijd dan naar de gele parkeerplaats.
Je kunt er vanuit gaan dat de kaart altijd een zwarte rand heeft, en verder geen zwart gebruikt.

Je kunt de software eerst ontwikkelen met een gesimuleerde robot, en daarna uit laten voeren door de
EV3 met een differential drive en een kleurensensor.

Hoe je te werk gaat:

* Zorg dat je de theorie van Les 1 op Udacity goed begrijpt

* Lees de python bestanden door zodat je weet waar je alles kunt vinden

* Maak daarna het Markov filter werkend:
    * Ga in eerste instantie er vanuit dat je altijd op dezelde plek in noordelijke richting start
    * Ga in eerste instantie er vanuit dat je robot perfect beweegt
    * Denk er daarna over na hoe je bewegingsonzekerheid programmeert
    * Bedenk nu een oplossing voor de orientaties (HINT: je kunt meerdere Markovs instatieren)

* Bedenk als laatst een strategie om je robot naar de 'parkeerplaats' te laten rijden.

Bestanden:

* histogram_weekopdracht.py: dit bestand, waarin je het filter programmeert
* robot.py: deze heb je pas nodig als je de EV3 gebruikt
* test_plattegrond.txt: een testkaart. het formaat staat uitgelegd in de functie load_map als je zelf ook kaarten wil maken

NB.
In dit bestand vind je TODO's op de plaatsen waar je aanpassingen moet doen en aanwijzingen (in pygame kan je
die makkelijk vinden doordat ze blauw in de kantlijn staan)


"""
import csv
import time
import random
from histogram_filter import HistogramFilter
from markov import Markov
from colors import Colors
from orientation import Orientation

SIMULATION = False

if SIMULATION:
    from robot import Robot

# Helper functies
def load_map(filename):
    """
    Laad de kaart uit een tekstbestand waarvan de colommen puntkomma en de rijen met enters gescheiden zijn, bijv:
    0;3;4;0
    0;4;3;0

    filename = naam tekstbestand
    """
    color_mapper = {}

    # Kleuren in kaartformaat
    color_mapper[0] = Colors.WHITE  # 0=wit
    color_mapper[1] = Colors.BLACK  # 1=zwart
    color_mapper[2] = Colors.RED  # 2=rood
    color_mapper[3] = Colors.GREEN  # 3=groen
    color_mapper[4] = Colors.BLUE  # 4=blauw
    color_mapper[5] = Colors.YELLOW  # 5=geel

    world = []

    with open(filename) as tsv:

        for tiles in csv.reader(tsv, delimiter=";"):
            row = []
            for tile in tiles:
                if tile == '':
                    continue  # extra delimiter at end of row, ignore
                row.append(color_mapper[int(tile)])

            world.append(row)

    return world

# Laad de juiste kaart
start_orientation = Orientation.NORTH
world = load_map("assets/test_plattegrond.txt")
robot = None

# Verbind met de robot Kies tussen echte of gesimuleerde robot
if SIMULATION:
    robot = Robot()
else:
    robot = HistogramFilter(world, 6, 4, start_orientation)
    robot.draw()

robot.connect_color()
markov = Markov(world, start_orientation, "rddesmit")
found = False

while not found:
    location = markov.current_estimate()
    destination = (1, 1)

    # drive
    robot.drive(0.10)
    markov.move()

    # rotate
    direction = Orientation.calculate_direction((location[1], location[2]), destination)
    while direction != markov._orientation:
        rotate_direction = Orientation.rotate(markov._orientation, direction)

        if rotate_direction == Orientation.LEFT:
            markov.rotate_left()
            robot.turn_left()
            time.sleep(3)
        elif rotate_direction == Orientation.RIGHT:
            markov.rotate_right()
            robot.turn_right()
            time.sleep(3)
        else:
            pass

    # calculate
    time.sleep(2)
    measurement = robot.sense_color()
    markov.update(measurement)

    if measurement == Colors.YELLOW:
        if robot.sense_color() == Colors.YELLOW:
            found = True
            print "found"

    print markov
    time.sleep(1)