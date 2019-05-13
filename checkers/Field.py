from enum import Enum


class Field(Enum):
    WHITE = 0
    BLACK = 1
    BLACK_FIELD_BLUE_PAWN = 2
    BLACK_FIELD_RED_PAWN = 3


class Player(Enum):
    WHITE = 0
    BLACK = 1
    WHITE_CAPTURE = 2
    BLACK_CAPTURE = 3
