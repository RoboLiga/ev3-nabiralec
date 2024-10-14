from enum import Enum


class State(Enum):
    """
    Stanja robota.
    """

    def __str__(self):
        return str(self.name)
    IDLE = 0
    TURN = 1
    DRIVE_STRAIGHT = 2
    LOAD_NEXT_TARGET = 3


class Point():
    """
    Točka na poligonu.
    """
    # TODO: implement __add__, __sub__, __eq__

    def __init__(self, position):
        self.x = position['x']
        self.y = position['y']

    def __str__(self):
        return '('+str(self.x)+', '+str(self.y)+')'
