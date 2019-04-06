import cv2
import argparse
import imutils
import numpy as np
from Field import Field
import requests
from matplotlib import pyplot as plt

STANDARD_DEVIATION = 20
def detectShape(c):
    # initialize the shape name and approximate the contour
    shape = None
    peri = 0.04 * cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, peri, True)
    # if the shape has 4 vertices, it is either a square or
    # a rectangle
    if len(approx) == 4:
        # a square will have an aspect ratio that is approximately
        # equal to one, otherwise, the shape is a rectangle
        shape = "square"  # if ar >= 0.95 and ar <= 1.05 else "rectangle"

    # # otherwise, we assume the shape is a circle
    else:
        shape = "circle"

    # return the name of the shape
    return shape

def findFields(image):
    imageBlack = image.copy()
    imageWhite = image.copy()

    gray = cv2.cvtColor(imageBlack, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 80, 255, cv2.THRESH_BINARY_INV)[1]
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.erode(thresh, kernel, iterations=1)
    # cv2.imshow("1thresh", thresh)
    # find contours in the thresholded imageBlack and initialize the
    # shape detector
    cnts1 = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    # contures of black fields
    cnts = imutils.grab_contours(cnts1)

    imageWhite = cv2.bitwise_not(imageWhite)
    gray = cv2.cvtColor(imageWhite, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY_INV)[1]
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.erode(thresh, kernel, iterations=1)
    # cv2.imshow("2thresh", thresh)
    # find contours in the thresholded blurred and initialize the
    # shape detector
    cnts2 = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)

    # add contures of white fields
    cnts = imutils.grab_contours(cnts2) + cnts
    cnts.reverse()
    if len(cnts) != 64:
        return None
    print("refreshed")

    cntsSorted = []
    values = []
    for i in range(len(cnts)-1):
        if i % 2 == 0:
            cntsSorted.append(cnts[int(i/2)])
            values.append(Field.BLACK)
        else:
            cntsSorted.append(cnts[32 + int(i/2)])
            values.append(Field.WHITE)


    pointsOfFields = []
    for c in cntsSorted:
        shape = detectShape(c)
        if shape == 'square':
            # cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            x = 0
            y = 0
            count = 0
            for t in c:
                x = x + t[0][0]
                y = y + t[0][1]
                count = count + 1
            x = int(x / count)
            y = int(y / count)
            pointsOfFields.append([x, y])
    # cv2.imshow("fields", image)
    return pointsOfFields

def findPawns(image, threshold):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY)[1]
    # cv2.imshow("pawnsThreshBeforeErode"+str(threshold), thresh)
    # kernel = np.ones((5, 5), np.uint8)
    # thresh = cv2.erode(thresh, kernel, iterations=2)
    # cv2.imshow("pawnsThresh" + str(threshold), thresh)

    # find contours in the thresholded imageBlack and initialize the
    # shape detector
    cnts1 = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    # contures of black fields
    cnts = imutils.grab_contours(cnts1)

    cnts.reverse()
    # print(str(threshold),len(cnts))

    pointsOfPawns = []
    for c in cnts:
        shape = detectShape(c)
        if shape == 'circle':
            x = 0
            y = 0
            count = 0
            for t in c:
                x = x + t[0][0]
                y = y + t[0][1]
                count = count + 1
            x = int(x/count)
            y = int(y/count)
            pointsOfPawns.append([x, y])
    #         cv2.circle(image, (x, y), 15, (255, 0, 0), 2)
    #
    # cv2.imshow("circle", image)

    return pointsOfPawns

def checkIfPawnOnField(fields, pawnsBlue, pawnsRed, image):
    result = []
    for i in range(64):
        if i % 2 == 0:
            result.append(Field.BLACK)
        else:
            result.append(Field.WHITE)

    for id, field in enumerate(fields):
        for pawn in pawnsBlue:
            if abs(field[0] - pawn[0]) <= 20 and abs(field[1] - pawn[1]) <= STANDARD_DEVIATION:
                cv2.circle(image, (field[0], field[1]), 10, (255, 0, 255), 3)
                result[id] = Field.BLACK_FIELD_BLUE_PAWN
                # print("blue")
        for pawn in pawnsRed:
            if abs(field[0] - pawn[0]) <= 20 and abs(field[1] - pawn[1]) <= STANDARD_DEVIATION:
                cv2.circle(image, (field[0], field[1]), 10, (255, 255, 0), 3)
                result[id] = Field.BLACK_FIELD_RED_PAWN
                # print("red")

    print(result)


def findChessboard(image):
    ULx = None
    ULy = None
    URx = None
    URy = None
    DLx = None
    DLy = None
    DRx = None
    DRy = None

    markersNames = ('images/DOWN_LEFT.png', 'images/UP_RIGHT.png', 'images/UP_LEFT.png', 'images/DOWN_RIGHT.png')

    # id is one of the corners of detected image that we need
    img2 = image.copy()  # trainImage
    for id, markerName in enumerate(markersNames):
        img1 = cv2.imread(markerName, 0)  # queryImage

        MIN_MATCH_COUNT = 5

        # Initiate SIFT detector
        sift = cv2.xfeatures2d.SIFT_create()

        # find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(img1, None)
        kp2, des2 = sift.detectAndCompute(img2, None)

        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)

        flann = cv2.FlannBasedMatcher(index_params, search_params)

        matches = flann.knnMatch(des1, des2, k=2)

        # store all the good matches as per Lowe's ratio test.
        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)

        if len(good) > MIN_MATCH_COUNT:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            h, w = img1.shape
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)

            if id == 0:
                DRx = [np.int32(dst)[id]][0][0][0]
                DRy = [np.int32(dst)[id]][0][0][1]
            elif id == 1:
                URx = [np.int32(dst)[id]][0][0][0]
                URy = [np.int32(dst)[id]][0][0][1]
            elif id == 2:
                ULx = [np.int32(dst)[id]][0][0][0]
                ULy = [np.int32(dst)[id]][0][0][1]
            elif id == 3:
                DLx = [np.int32(dst)[id]][0][0][0]
                DLy = [np.int32(dst)[id]][0][0][1]


    pts1 = np.float32([[ULx, ULy], [URx, URy], [DLx, DLy], [DRx, DRy]])
    pts2 = np.float32([[0, 0], [500, 0], [0, 500], [500, 500]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(image, M, (500, 500))
    return result

def main():
    url = "http://192.168.1.66:8080/shot.jpg"
    while True:
            img_resp = requests.get(url)
            img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
            img = cv2.imdecode(img_arr, -1)

            try:
                img = findChessboard(img)
                # Converts images from BGR to HSV
                img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                # Find blue pawns
                lowerBlue = np.array([110, 100, 50], dtype='uint8')
                upperBlue = np.array([130, 255, 255], dtype='uint8')
                mask = cv2.inRange(img, lowerBlue, upperBlue)
                res = cv2.bitwise_and(img, img, mask=mask)
                bluePawns = findPawns(image=res, threshold=50)


                # Find red pawns
                lowerRed1 = np.array([0, 70, 50], dtype='uint8')
                upperRed1 = np.array([10, 255, 255], dtype='uint8')
                mask1 = cv2.inRange(img, lowerRed1, upperRed1)
                lowerRed2 = np.array([170, 70, 50], dtype='uint8')
                upperRed2 = np.array([180, 255, 255], dtype='uint8')
                mask2 = cv2.inRange(img, lowerRed2, upperRed2)

                res = cv2.bitwise_or(cv2.bitwise_and(img, img, mask=mask1), cv2.bitwise_and(img, img, mask=mask2))
                redPawns = findPawns(image=res, threshold=130)

                img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
                fields = findFields(img)
                checkIfPawnOnField(fields, bluePawns, redPawns, img)
                cv2.imshow("Wykryte pola", img)
                if img is None:
                    continue
                # cv2.imshow("Wykryte pola", img)
            except:
                continue
            if cv2.waitKey(1) == 27:
                break

    # img2 = cv2.imread("images/chessboardARUCO_2.png", 1)
    # img = findChessboard(img2)
    #
    # # Find blue pawns
    # lowerBlue = np.array([0, 0, 0], dtype='uint8')
    # upperBlue = np.array([255, 50, 50], dtype='uint8')
    # mask = cv2.inRange(img, lowerBlue, upperBlue)
    # res = cv2.bitwise_and(img, img, mask=mask)
    # bluePawns = findPawns(image=res, threshold=30)
    #
    # # Find red pawns
    # lowerRed = np.array([0, 0, 0], dtype='uint8')
    # upperRed = np.array([50, 50, 255], dtype='uint8')
    # mask = cv2.inRange(img, lowerRed, upperRed)
    # res = cv2.bitwise_and(img, img, mask=mask)
    # redPawns = findPawns(image=res, threshold=50)
    #
    # fields = findFields(img)
    # checkIfPawnOnField(fields, bluePawns, redPawns, img)
    # cv2.imshow("Wykryte pola", img)
    # cv2.waitKey(0)

    # pawnsBlue = findPawns(img, 30)
    # pawnsRed = findPawns(img, 60)
    # fields = findFields(img)
    # checkIfPawnOnField(fields, pawnsBlue, pawnsRed, img)
    # cv2.imshow("Wykryte pola", img)
    # cv2.waitKey(0)

# Function to calculate proportion of a certain channel
def colour_frac(color):
    return np.sum(color)/np.sum(intensity)

if __name__ == '__main__':
    main()
    # img = cv2.imread("images/blue.png", 1)
    # cv2.imshow("obrazek", img)
    #
    # # Extract each colour channel
    # blue, green, red = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    # # Total red+green+blue intensity
    # intensity = img.sum(axis=2)
    # # Calculate the proportion of each colour
    # red_fraction = colour_frac(red)
    # green_fraction = colour_frac(green)
    # blue_fraction = colour_frac(blue)
    #
    # sum_colour_fraction = red_fraction + green_fraction + blue_fraction
    # print('Red fraction: {}'.format(red_fraction))
    # print('\nGreen fraction: {}'.format(green_fraction))
    # print('\nBlue fraction: {}'.format(blue_fraction))
    # print('\nRGB sum: {}'.format(sum_colour_fraction))
    # print(red.shape == green.shape == blue.shape)
    # cv2.waitKey(0)