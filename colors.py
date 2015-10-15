# De Color constants van de EV3 (niet compleet)


class Colors:

    def __init__(self):
        pass

    BLACK = 0
    UNKNOWN = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4
    RED = 5
    WHITE = 6
    UNKNOWN2 = 7  # oranje?

    # Color-tabel om de kaart te tekenen in de simulatie
    COLOR_TO_RGB = {
        BLACK: (0, 0, 0),
        UNKNOWN: (0, 0, 0),
        BLUE: (0, 0, 255),
        GREEN: (0, 255, 0),
        UNKNOWN2: (0, 0, 0),
        RED: (255, 0, 0),
        WHITE: (255, 255, 255),
        YELLOW: (255, 255, 0)
    }

    color_names = ["Black", "None", "Blue", "Green", "Yellow", "Red", "White", "None2"]