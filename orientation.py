import random

class Orientation:

    def __init__(self):
        pass

    orientation_names = ["North", "East", "South", "West"]
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    direction_names = ["Left", "Right"]
    NONE = 0
    LEFT = -1
    RIGHT = 1

    @staticmethod
    def calculate_direction((ly, lx), (dy, dx)):
        def orientate_x():
            return Orientation.WEST if lx > dx else Orientation.EAST

        def orientate_y():
            return Orientation.NORTH if ly > dy else Orientation.SOUTH

        # decide random whether or not to solve x-axis first
        direction = random.randint(0, 1)
        return orientate_x() if direction == 0 or ly == dy else orientate_y()

    @staticmethod
    def rotate(c_orientation, d_orientation):
        if c_orientation - d_orientation == 0:
            return Orientation.NONE
        elif c_orientation - d_orientation >= 1:
            return Orientation.LEFT
        else:
            return Orientation.RIGHT