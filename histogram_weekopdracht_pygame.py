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
from histogram_filter_simulated_robot import HistogramFilterSimulatedRobot
from markov import Markov
from colors import Colors
from orientation import Orientation

# TODO: Zet SIMULATION op False om de EV3 aan te sturen, en True om een simulatie te doen


SIMULATION = True

if not SIMULATION:
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
# TODO: initialiseer Markov met de kaart

if not SIMULATION:
    robot = Robot()
else:
    robot = HistogramFilterSimulatedRobot(world, 6, 4, start_orientation)
    robot.draw()

robot.connect_color()

markov = Markov(world, start_orientation, "rddesmit")

found = False

while not found:
    def calculate_direction((ly, lx), (dy, dx)):
        if ly == dy:
            # we are on the correct row, navigate to the correct column
            return Orientation.WEST if lx > dx else Orientation.EAST
        else:
            # we are NOT on te correct row, navigate to the correct row
            return Orientation.NORTH if ly > dy else Orientation.SOUTH

    def rotate(c_orientation, d_orientation):
        if c_orientation - d_orientation == 0:
            pass
        elif c_orientation - d_orientation >= 1:
            robot.rotate(-1)
            markov.rotate(-1)
        else:
            robot.rotate(1)
            markov.rotate(1)

    location = markov.current_estimate()
    destination = (3, 6)


    # TODO: beweeg de robot en update de Markov (probeer eerst vast of random route,
    # denk daarna na over een strategie die je bij de parkeerplaats brengt)
    # drive
    robot.drive(0.10)
    markov.move()

    # rotate
    direction = calculate_direction((location[1], location[2]), destination)
    while markov._orientation != direction:
        rotate(markov._orientation, direction)

    # TODO: doe een measurement en update de Markov
    # calculate
    measurement = robot.sense_color()
    markov.update(measurement)

    if measurement == Colors.YELLOW:
        if robot.sense_color() == Colors.YELLOW:
            found = True
            print "found"

    # for x in markov._p:
    #     print x

    print markov
    time.sleep(3)








# TODO: bekijk je estimate en besluit of je kunt stoppen of terug moet naar de meting
