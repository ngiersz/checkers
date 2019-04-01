import cv2
import os
from enum import Enum


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

if __name__ == '__main__':
    print(cv2.__version__)
    pattern = cv2.imread('pattern.png', cv2.IMREAD_GRAYSCALE)
    print(pattern.shape)
    ret, left_corners = cv2.findChessboardCorners(pattern, (6, 9))
    # print(left_corners)
    # print(ret)
    pattern_with_corners = pattern
    for corner in left_corners:
        print(corner)
        coord_a = 0
        coord_b = 0
        for x in corner:
            first = True
            for y in x:
                if first:
                    coord_a = y
                    first = False
                else:
                    coord_b = y
        # print('(' + str(coord_a) + ', ' + str(coord_b) + ')')
        cv2.circle(pattern_with_corners, (coord_a, coord_b), 10, (255, 0, 0), -1)
        # cv2.circle(img, (447, 63), 63, (0, 0, 255), -1)

    save_image(pattern_with_corners, 'pattern_with_corners')


