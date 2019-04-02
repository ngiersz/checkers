"""
CONFIG
Default checkers_window  settings
"""
SIZE = (1920, 1080)  # Size of checkers window
RECT_SIZE = SIZE[0] / 20  # size of fields on chessboard
CHECKER_SIZE = SIZE[0] / 30  # size of checker
CAMERA_H = int(SIZE[1] / 2)  # height of camera window
CAMERA_W = int(SIZE[0] / 2.5)  # width of camera window
RECT_OFFSET_X = SIZE[0] / 2  # offset for field on x axis
RECT_OFFSET_Y = SIZE[0] / 30  # offset for field on y axis
CHECKER_OFFSET_X = RECT_OFFSET_X + (RECT_SIZE - CHECKER_SIZE) / 2  # offset for checker on x axis
CHECKER_OFFSET_Y = RECT_OFFSET_Y + (RECT_SIZE - CHECKER_SIZE) / 2  # offset for checker on y axis
CAMERA_OFFSET_X = SIZE[0]/30
CAMERA_OFFSET_Y = SIZE[1]/30
