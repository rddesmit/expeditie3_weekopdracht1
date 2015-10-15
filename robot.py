# coding=utf-8
import rpyc
import math
import random

############### Zet deze waarden goed voor je robot ###################

# Het ip-adres van de ev3 die bestuurd wordt

# TODO: Aanpassen voor jouw robot
IP_EV3 = "192.168.0.10"
# Straal (as tot grond) van de wielen in meters(!)
WHEEL_RADIUS = 1.0
# Afstand tussen de wielen in meters
WHEEL_BASE = 1.0
# Aantal 'tikken' van de rotary counter in een wiel, bij de EV3 is die 360 tikken per omwenteling
WHEEL_TICKS360 = 360.


############### Hieronder niks aanpassen ################################


# Bereken de constanten die nodig zijn voor het rijden
TICKS_PER_METER = WHEEL_TICKS360 / ( 2. * math.pi * WHEEL_RADIUS )
TICKS_PER_RAD = (WHEEL_BASE / 2) * TICKS_PER_METER


# Verbind met de EV3, verwijder deze twee regels als je je programma direct op de EV3 draait
c = rpyc.classic.connect(IP_EV3)
ev3dev = c.modules.ev3dev



class Robot:
    """

    Robot-class

    Met deze class kan je een differential drive (twee onafhankelijk bestuurbare voorwielen, en een achter een zwenkwiel
    of ball caster) aansturen met de EV3 of in direct-drive modus een robot die niet kan sturen en met 1 motor voor of
    achteruit rijdt.

    Motoren:

    Links = outB
    Rechts = outC
    Beide wielen = outA (alleen beschikbaar in direct drive)


    """

    def __init__(self, extra_motor = False):
        """
        Default is extra_motor false (normale differentioal drive robot), zet deze True als je een motor voor beide
        wielen aansluit (alleen nodig voor de opdracht van week 3)
        """

        # Connect to motors

        motor_left = ev3dev.large_motor('outB')
        motor_left.reset()
        motor_right = ev3dev.large_motor('outC')
        motor_right.reset()
        self._motors = [motor_left, motor_right]
        self._motor_running = [False, False]

        if (extra_motor):
            motor_extra = ev3dev.large_motor('outD')
            motor_extra.reset()
            self._motors.append(motor_extra)
            self._motor_running.append(False)

        self._power = 40
        self._speed = 275


    def connect_color(self):
        """
        Roep deze eerst aan als je de color sensor wil gebruiken
        """
        self._color_sensor = ev3dev.color_sensor();
        assert self._color_sensor.connected
        self._color_sensor.mode = 'COL-COLOR'

    def connect_ultrasone(self, ports = ['in2:i2c1'], offsets = [10]):
        """
        Roep deze eerst aan als je de ultrasone sensor wil gebruiken

        Default = één sensor, verbonden aan in2, die 10 cm vanaf het middelpunt van de robot staat.
        """
        self._ultrasone = []
        for sensor in range(len(ports)):
            u = ev3dev.ultrasonic_sensor(ports[sensor]);
            offset = 0
            if len(offsets) > 0:
                offset = offsets[sensor]
            self._ultrasone.append((u, offset))

    def connect_ir(self, ports = ['in1'], offsets = [10]):
        """
        Roep deze eerst aan als je de ir sensor wil gebruiken

        Default = één sensor, verbonden aan in1, die 10 cm vanaf het middelpunt van de robot staat.
        """
        self._ir = []

        for sensor in range(len(ports)):
            i = ev3dev.infrared_sensor(ports[sensor]);
            i.mode = 'IR-PROX'
            offset = 0
            if len(offsets) > 0:
                offset = offsets[sensor]
            self._ir.append((i, offset))

    def turn(self, rad):
        """
        Draai de robot een aantal radialen (2 pi radialen = 360 graden). Plus = rechts, min = links
        """
        # calc ticks
        ticks = int(float(rad) * TICKS_PER_RAD)
        self.turn_motors((ticks, -ticks))

    def turn_right(self, rad=0.5*math.pi):
        """
        Draai de robot een aantal radialen naar rechts (2 pi radialen = 360 graden).

        Default = 0.5pi radialen / 90 graden
        """
        self.turn(rad)

    def turn_left(self, rad=0.5*math.pi):
        """
        Draai de robot een aantal radialen naar links (2 pi radialen = 360 graden).

        Default = 0.5pi radialen / 90 graden
        """
        self.turn(-rad)

    def drive(self, dist=0.10):
        """
        Rijd de robot een aantal meter. Plus = vooruit, min = achteruit.
        """
        # calc ticks
        ticks = int(float(dist) * TICKS_PER_METER)
        self.turn_motors((ticks, ticks))

    def turn_motors(self, ticks):
        """
        Draai de motoren een aantal ticks.

        Alleen voor intern gebruik.
        """
        self._motors[0].stop_command = "brake"
        self._motors[1].stop_command = "brake"

        self._motors[0].position_sp = ticks[0]
        self._motors[1].position_sp = ticks[1]

        self._motors[0].speed_sp = self._speed
        self._motors[1].speed_sp = self._speed

        # cannot figure out how to start motors at same time, so start them
        # in random order
        if (random.random() > 0.5):
            self._motors[0].run_to_rel_pos(speed_regulation_enabled='on')
            self._motors[1].run_to_rel_pos(speed_regulation_enabled='on')
        else:
            self._motors[1].run_to_rel_pos(speed_regulation_enabled='on')
            self._motors[0].run_to_rel_pos(speed_regulation_enabled='on')

    def direct_drive(self, duty_cycles = [0, 0], motors = [0,1]):
        """
        Stuur een bepaalde kracht naar de motoren.

        Default naar motor 0 en 1 (= B en C), maar kan ook naar 2 (= A)

        duty_cycles = lijst met percentages
        motors = lijst met motors
        """
        for motor_number in range(len(motors)):
            motor = motors[motor_number]
            self._motors[motor].duty_cycle_sp = duty_cycles[motor_number]

    def direct_drive_init(self, motors = [0,1]):
        """
        Initialiseer de motors voor direct drive

        Default naar motor 0 en 1 (= B en C), maar kan ook naar 2 (= A)

        duty_cycles = lijst met percentages
        motors = lijst met motors
        """
        for motor in motors:
            self._motors[motor].duty_cycle_sp = 0
            self._motors[motor].run_direct(speed_regulation_enabled='off', stop_command='coast')

    def direct_drive_brake(self, motors = [0,1]):
        """
        Zet de direct drive motors uit.

        Default naar motor 0 en 1 (= B en C), maar kan ook naar 2 (= A)

        duty_cycles = lijst met percentages
        motors = lijst met motors
        """
        for motor in motors:
            self._motors[motor].stop(speed_regulation_enabled='off', stop_command='coast')

    def sense_color(self):
        """
        Detecteer kleur

        BLACK = 0
        UNKNOWN = 1
        BLUE = 2
        GREEN = 3
        UNKNOWN2 = 4
        RED = 5
        WHITE = 6
        YELLOW = 7
        """
        return self._color_sensor.value()

    def sense_ultrasone(self):
        """
        Meet ultrasone afstanden. Geeft lijst met afstanden van de sensors in cm terug
        """
        measurements = []
        for sensor in self._ultrasone:
            # max 100 (for compatibility with ir)
            measurements.append(sensor[1] + min(100.0, float(sensor[0].value())))

        return measurements

    def sense_ir(self):
        """
        Meet ir afstanden. Geeft lijst met afstanden van de sensors in cm terug
        """
        measurements = []
        for sensor in self._ir:
            measurements.append(sensor[1] + min(100.0, float(sensor[0].value())))

        return measurements

