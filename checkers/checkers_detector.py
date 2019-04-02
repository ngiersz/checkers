import cv2
import checkers.ShapeDetector as ShapeDetector
import imutils
import numpy as np


def find_chessboard(image):
    """
            Function that finds fields on the image and draws
            them on it
            returns:
                image as cv2 frame
    """
    imageBlack = image.copy()
    imageWhite = image.copy()

    gray = cv2.cvtColor(imageBlack, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY_INV)[1]
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.erode(thresh, kernel, iterations=1)
    #cv2.imshow("1thresh", thresh)
    # find contours in the thresholded imageBlack and initialize the
    # shape detector
    cnts1 = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    # contures of black fields
    cnts = imutils.grab_contours(cnts1)

    imageWhite = cv2.bitwise_not(imageWhite)
    gray = cv2.cvtColor(imageWhite, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 80, 255, cv2.THRESH_BINARY_INV)[1]
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.erode(thresh, kernel, iterations=1)
    #cv2.imshow("2thresh", thresh)
    # find contours in the thresholded blurred and initialize the
    # shape detector
    cnts2 = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)

    # add contures of white fields
    cnts = imutils.grab_contours(cnts2) + cnts
    cnts.reverse()

    # cntsSorted = []
    # for i in range(len(cnts)-1):
    #     if i % 2 == 0:
    #         cntsSorted.append(cnts[int(i/2)])
    #     else:
    #         cntsSorted.append(cnts[32 + int(i/2)])

    sd = ShapeDetector.ShapeDetector()

    # cntsSorted[0][1][0][1] = 99
    # print(cntsSorted[0])
    # print(cntsSorted[0][0][0][0])
    # g = image[cntsSorted[0][0][0][1]:cntsSorted[0][2][0][1],cntsSorted[0][0][0][0]:cntsSorted[0][2][0][0]]
    # cv2.imshow("pierwsze pole", g)
    # loop over the contours
    for c in cnts:
        shape = sd.detect(c)
        if shape == 'square':
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)

        # compute the center of the contour, then detect the name of the
        # shape using only the contour
        # M = cv2.moments(c)
        # cX = int((M["m10"] / M["m00"]))
        # cY = int((M["m01"] / M["m00"]))
        # cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
        #             0.5, (255, 255, 255), 2)

    return image





