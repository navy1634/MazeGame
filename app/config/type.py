from enum import IntEnum, StrEnum


class Color(StrEnum):
    RED = "red"
    BLUE = "blue"


class DIRECTION(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class Maze3DColor(StrEnum):
    LAYER0 = "#a5bcf9"
    LAYER1 = "#626e97"
    LAYER2 = "#535c7f"
    LAYER3 = "#404864"
    LAYER4 = "#37d86e"
