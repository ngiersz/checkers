import cv2
import os
from enum import Enum
import numpy as np


def save_image(img, prefix):
    suffix = 1
    found = False
    extension = '.png'
    while not found:
        name = str(prefix) + str(suffix) + str(extension)
        exists = os.path.isfile(name)
        if exists:
            suffix = suffix + 1
        else:
            found = True
            cv2.imwrite(name, img)
            print('Image saved to ' + str(name))


class Field(Enum):
    WHITE = 1
    BLACK = 2
    BLACK_WITH_PLAYER_1 = 3
    BLACK_WITH_PLAYER_2 = 4


board_shape = [8, 8]
board = np.array(board_shape)


if __name__ == '__main__':
    pattern = cv2.imread('pattern.png', cv2.IMREAD_GRAYSCALE)
    ret, left_corners = cv2.findChessboardCorners(pattern, (board_shape[0]-1, board_shape[1]-1))
    pattern_with_corners = pattern
    for corner in left_corners:
        coord = np.array([int(corner.item((0, 0))), int(corner.item((0, 1)))])
        print(coord)
        cv2.circle(pattern_with_corners, (coord[0], coord[1]), 10, (255, 0, 0), -1)

    save_image(pattern_with_corners, 'pattern_with_corners')


