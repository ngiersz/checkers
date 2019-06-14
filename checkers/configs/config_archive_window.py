import cv2
import pygame as pg
from checkers.fields import Field
"""
CONFIG
Default checkers_window  settings
"""
SIZE = (1920, 1080)  # Size of checkers window
RECT_SIZE = int(SIZE[0] / 20)  # size of fields on chessboard
PAWN_SIZE = SIZE[0] / 30  # size of checker
SELECT_GAME_WIDTH_TEXT = int(SIZE[0] / 5)
SELECT_GAME_HEIGHT_TEXT = int(SIZE[0] / 20)
SELECT_GAME_WIDTH_B = int(SIZE[0] / 10)
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
BLACK_FIELD = cv2.cvtColor(cv2.imread("images/black.jpg"), 3)
WHITE_FIELD = cv2.cvtColor(cv2.imread("images/white.jpg"), 3)
RED_PAWN = cv2.cvtColor(cv2.imread("images/red_pawn.png"), 3)
BLUE_PAWN = cv2.cvtColor(cv2.imread("images/blue_pawn.png"), 3)
RED_QUEEN = cv2.cvtColor(cv2.imread("images/red_queen.png"), 3)
BLUE_QUEEN = cv2.cvtColor(cv2.imread("images/blue_queen.png"), 3)
BACKGROUND = cv2.cvtColor(cv2.imread("images/background.jpg"), 3)
WINDOW_BACKGROUND = cv2.cvtColor(cv2.imread("images/window_background.jpg"), 3)
BOARD_BACKGROUND = cv2.cvtColor(cv2.imread("images/window_background.jpg"), 3)
BUTTON = cv2.rotate(cv2.cvtColor(cv2.imread("images/button_menu.jpg"), 3), 2)
BUTTON2 = cv2.rotate(cv2.cvtColor(cv2.imread("images/button_menu2.jpg"), 3), 2)
BUTTON3 = cv2.rotate(cv2.cvtColor(cv2.imread("images/button_menu3.jpg"), 3), 2)

BOARD_SIZE = RECT_SIZE*9

BAR_SIZE_Y = 100

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


