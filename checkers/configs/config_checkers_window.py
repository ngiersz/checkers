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
CAMERA_H = int(SIZE[1] / 2)  # height of camera window
CAMERA_W = int(SIZE[0] / 2.5)  # width of camera window
RECT_OFFSET_X = SIZE[0] / 2  # offset for field on x axis
RECT_OFFSET_Y = SIZE[0] / 30  # offset for field on y axis
PAWN_OFFSET_X = RECT_OFFSET_X + (RECT_SIZE - PAWN_SIZE) / 2  # offset for checker on x axis
PAWN_OFFSET_Y = RECT_OFFSET_Y + (RECT_SIZE - PAWN_SIZE) / 2  # offset for checker on y axis
CAMERA_OFFSET_X = SIZE[0]/30
CAMERA_OFFSET_Y = SIZE[1]/30
SELECT_NAME_HEIGHT = int(SIZE[0] / 20)
SELECT_NAME_WIDTH = int(SIZE[0] / 5)
SELECT_NAME_OFFSET_X = int(SIZE[0] / 8)
SELECT_NAME_OFFSET_Y = (int(SIZE[1]) - SELECT_NAME_HEIGHT * 4)
SAVE_GAME_HEIGHT = int(SIZE[0] / 20)
SAVE_GAME_WIDTH = int(SIZE[0] / 5)
SAVE_GAME_OFFSET_X = int(SIZE[0] - int(SIZE[0] / 3))
SAVE_GAME_OFFSET_Y = (int(SIZE[1]) - SAVE_GAME_HEIGHT)
SET_STATE_HEIGHT = int(SIZE[0] / 20)
SET_STATE_WIDTH = int(SIZE[0] / 5)
SET_STATE_OFFSET_X = int(SIZE[0] / 8)
SET_STATE_OFFSET_Y = (int(SIZE[1]) - SET_STATE_HEIGHT)
MOVE_COMMUNICATE_HEIGHT = int(SIZE[0] / 20)
MOVE_COMMUNICATE_WIDTH = int(3 * SIZE[0] / 5)
MOVE_COMMUNICATE_OFFSET_X = int(int(SIZE[0] / 3))
MOVE_COMMUNICATE_OFFSET_Y = (int(SIZE[1]) - SAVE_GAME_HEIGHT*2 - 25)
BLACK_FIELD = cv2.cvtColor(cv2.imread("black.jpg"), 3)
WHITE_FIELD = cv2.cvtColor(cv2.imread("white.jpg"), 3)
WHITE_PAWN = cv2.cvtColor(cv2.imread("white_pawn.png"), 3)
BLACK_PAWN = cv2.cvtColor(cv2.imread("black_pawn.png"), 3)
FONT = pg.font.SysFont('Comic Sans MS', 32)
NO_NAME = 'Choose Name'

BEGIN_STATE = [[Field.BLACK, Field.WHITE, Field.BLACK_FIELD_RED_PAWN, Field.WHITE, Field.BLACK_FIELD_RED_PAWN, Field.WHITE, Field.BLACK, Field.WHITE],
               [Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK],
               [Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE],
               [Field.WHITE, Field.BLACK_FIELD_BLUE_PAWN, Field.WHITE, Field.BLACK_FIELD_BLUE_PAWN, Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK],
               [Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE],
               [Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK],
               [Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE],
               [Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK, Field.WHITE, Field.BLACK]]
