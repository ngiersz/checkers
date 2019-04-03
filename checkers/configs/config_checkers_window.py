import cv2
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
BLACK_FIELD = cv2.cvtColor(cv2.imread("black.jpg"), 3)
WHITE_FIELD = cv2.cvtColor(cv2.imread("white.jpg"), 3)
WHITE_PAWN = cv2.cvtColor(cv2.imread("white_pawn.png"), 3)
BLACK_PAWN = cv2.cvtColor(cv2.imread("black_pawn.png"), 3)
