import cv2
import ShapeDetector
import argparse
import imutils
import time
import numpy as np

def show_webcam(cam, mirror=False):

    while True:
        ret_val, img = cam.read()
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        if mirror:
            img = cv2.flip(img, 1)
        img = findCheesboard(img)
        cv2.imshow('Chessboard', img)

        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()
    # ret_val, img = cam.read()
    # cv2.imshow("Asdasd",img)
    # cv2.waitKey(0)
    # return img


def findCheesboard(image):
    imageBlack = image.copy()
    imageWhite = image.copy()

    gray = cv2.cvtColor(imageBlack, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 130, 255, cv2.THRESH_BINARY_INV)[1]
    cv2.imshow("1thresh", thresh)
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.erode(thresh, kernel, iterations=1)
    # find contours in the thresholded imageBlack and initialize the
    # shape detector
    cnts1 = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    # contures of black fields
    cnts = imutils.grab_contours(cnts1)

    imageWhite = cv2.bitwise_not(imageWhite)
    gray = cv2.cvtColor(imageWhite, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 130, 255, cv2.THRESH_BINARY_INV)[1]
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.erode(thresh, kernel, iterations=2)
    cv2.imshow("2thresh", thresh)
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


def main():
    image = cv2.imread("hm.png")
    cam = cv2.VideoCapture(1)
    cam.set(3, 640)
    cam.set(4, 480)
    cam.set(5, 75)
    show_webcam(cam)
    # imageResult = findCheesboard(image)
    # cv2.imshow("Result", imageResult)
    # cv2.waitKey(0)
    # # while True:
    # while True:
    #     image = show_webcam(cam, mirror=False)
    #     cv2.imwrite("hm.png", image)
    # imageResult = findCheesboard(image)




if __name__ == '__main__':
    main()