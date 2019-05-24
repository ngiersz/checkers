import cv2
import pygame as pg
from checkers.Field import Field
"""
CONFIG
Default checkers_window  settings
"""
SIZE = (1920, 1080)  # Size of checkers window
RECT_SIZE = int(SIZE[0] / 20)  # size of fields on chessboard
PAWN_SIZE = SIZE[0] / 30  # size of checker
SELECT_GAME_WIDTH_TEXT = int(SIZE[0] / 5)
SELECT_GAME_HEIGHT_TEXT = int(SIZE[0] / 20)
SELECT_GAME_WIDTH_B = int(SIZE[0] / 15)
SELECT_GAME_HEIGHT_B = int(SIZE[0] / 20)
SELECT_GAME_OFFSET_Y = int(SIZE[1] / 2) - SELECT_GAME_HEIGHT_TEXT  # offset for game selecting options on Y
SELECT_GAME_OFFSET_X_T = int(SIZE[0] / 20)  # offset for game selecting options on X
SELECT_GAME_OFFSET_X_B = int(SIZE[0] / 20) +((SELECT_GAME_WIDTH_TEXT-SELECT_GAME_WIDTH_B)/2)  # offset for game selecting options on X

SELECT_MOVE_WIDTH = int(SIZE[0] / 10)
SELECT_MOVE_HEIGHT = int(SIZE[0] / 20)
SELECT_MOVE_OFFSET_Y = int(SIZE[1]) - int(SIZE[1] / 7)  # offset for game selecting options on Y
SELECT_MOVE_OFFSET_X = int(SIZE[0] / 2)  # offset for game selecting options on X

RECT_OFFSET_X = SIZE[0] / 2.8  # offset for field on x axis
RECT_OFFSET_Y = SIZE[0] / 30  # offset for field on y axis
PAWN_OFFSET_X = RECT_OFFSET_X + (RECT_SIZE - PAWN_SIZE) / 2  # offset for checker on x axis
PAWN_OFFSET_Y = RECT_OFFSET_Y + (RECT_SIZE - PAWN_SIZE) / 2  # offset for checker on y axis
CAMERA_OFFSET_X = SIZE[0]/30
CAMERA_OFFSET_Y = SIZE[1]/30
BLACK_FIELD = cv2.cvtColor(cv2.imread("black.jpg"), 3)
WHITE_FIELD = cv2.cvtColor(cv2.imread("white.jpg"), 3)
WHITE_PAWN = cv2.cvtColor(cv2.imread("white_pawn.png"), 3)
BLACK_PAWN = cv2.cvtColor(cv2.imread("black_pawn.png"), 3)
FONT = pg.font.SysFont('Comic Sans MS', 32)
FONT_TEXT = pg.font.SysFont('Comic Sans MS', 20)
NO_GAMES = "NoGamesSaved"

BEGIN_STATE = [[Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE],
               [Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK],
               [Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE],
               [Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK],
               [Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE],
               [Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK],
               [Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE],
               [Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK]]


