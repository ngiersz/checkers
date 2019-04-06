import cv2
import ShapeDetector
import argparse
import imutils
import numpy as np
from Field import Field
import requests


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
    print(len(cnts))
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


    sd = ShapeDetector.ShapeDetector()
    pointsOfFields = []
    for c in cntsSorted:
        shape = sd.detect(c)
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
    return pointsOfFields


def findPawns(image, threshold):
    imageBlack = image.copy()
    imageWhite = image.copy()

    gray = cv2.cvtColor(imageBlack, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY)[1]
    kernel = np.ones((5, 5), np.uint8)
    cv2.imshow("pawnsThreshBeforeErode"+str(threshold), thresh)
    thresh = cv2.erode(thresh, kernel, iterations=1)
    cv2.imshow("pawnsThresh"+str(threshold), thresh)
    # find contours in the thresholded imageBlack and initialize the
    # shape detector
    cnts1 = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    # contures of black fields
    cnts = imutils.grab_contours(cnts1)

    cnts.reverse()
    print(str(threshold),len(cnts))

    pointsOfPawns = []
    sd = ShapeDetector.ShapeDetector()
    for c in cnts:
        shape = sd.detect(c)
        if shape == 'circle':
            # cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
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
            # cv2.circle(image, (x, y), 15, (255, 0, 0), 2)
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
            if abs(field[0] - pawn[0]) <= 20 and abs(field[1] - pawn[1]) <= 20:
                cv2.circle(image, (field[0], field[1]), 10, (255, 0, 0), 3)
                result[id] = Field.BLACK_FIELD_BLUE_PAWN
                print("blue")
        for pawn in pawnsRed:
            if abs(field[0] - pawn[0]) <= 20 and abs(field[1] - pawn[1]) <= 20:
                cv2.circle(image, (field[0], field[1]), 10, (0, 255, 0), 3)
                result[id] = Field.BLACK_FIELD_RED_PAWN
                print("red")

    cv2.imshow("hehhe", image)
    print(result)

def main():
    url = "http://192.168.1.66:8080/shot.jpg"
    while True:
        img_resp = requests.get(url)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        img = cv2.imdecode(img_arr, -1)

        try:
            img = cv2.imread("images/chessboardARUCO.png", 1)
            img = findChessboard(img)
            pawnsBlue = findPawns(img, 10)
            pawnsRed = findPawns(img, 200)
            fields = findFields(img)
            checkIfPawnOnField(fields, pawnsBlue, pawnsRed, img)
            cv2.waitKey(0)
            if img is None:
                continue
            # cv2.imshow("Wykryte pola", img)
        except:
            continue
        if cv2.waitKey(1) == 27:
            break

    # img2 = cv2.imread("images/chessboardARUCO_2.png", 1)
    # img = findChessboard(img2)
    # pawnsBlue = findPawns(img, 30)
    # pawnsRed = findPawns(img, 60)
    # fields = findFields(img)
    # checkIfPawnOnField(fields, pawnsBlue, pawnsRed, img)
    # cv2.imshow("Wykryte pola", img)
    # cv2.waitKey(0)

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
    print(result.shape)
    return result


if __name__ == '__main__':
        main()
