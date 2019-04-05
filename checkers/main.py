import cv2
import ShapeDetector
import argparse
import imutils
import time
import numpy as np
from matplotlib import pyplot as plt
import requests


def show_webcam(cam, mirror=False):

    while True:
        ret_val, img = cam.read()

        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        if mirror:
            img = cv2.flip(img, 1)

        # img = searchChessboard(img)
        # img = findCheesboard(img)
        cv2.imshow('Chessboard', img)

        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()
    # ret_val, img = cam.read()
    # cv2.imshow("Asdasd",img)
    # cv2.waitKey(0)
    # return img


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


def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect

def main():
    # cam = cv2.VideoCapture(1)
    # cam.set(3, 640)
    # cam.set(4, 480)
    # cam.set(5, 75)
    # show_webcam(cam)

    # image = cv2.imread("chessboardARUCO.png", 0)
    # cv2.imshow("dsfsd", image)
    # cv2.waitKey(0)

    url = "http://192.168.1.66:8080/shot.jpg"
    while True:
        img_resp = requests.get(url)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        img = cv2.imdecode(img_arr, -1)

        try:
            img = findChessboard(img)
            img = findFields(img)
            if img is None:
                continue
            cv2.imshow("Wykryte pola", img)
        except:
            continue
        if cv2.waitKey(1) == 27:
            break


def findChessboard(image):
    ULx = None
    ULy = None
    URx = None
    URy = None
    DLx = None
    DLy = None
    DRx = None
    DRy = None



    markersNames = ('DOWN_LEFT.png', 'UP_RIGHT.png', 'UP_LEFT.png', 'DOWN_RIGHT.png')

    # id is one of the corners of detected image that we need
    img2 = image  # trainImage
    for id, markerName in enumerate(markersNames):
        img1 = cv2.imread(markerName, 0)  # queryImage

        MIN_MATCH_COUNT = 10

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
            matchesMask = mask.ravel().tolist()

            h, w = img1.shape
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)

            # img2 = cv2.polylines(img2, [np.int32(dst)], True, (255, 0, 0), 3, cv2.LINE_AA)

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

        else:
            # print("Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT))
            pass
            matchesMask = None

        # draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
        #                    singlePointColor=None,
        #                    matchesMask=matchesMask,  # draw only inliers
        #                    flags=2)
        #
        # img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)

    # result = image[URy:DRy, ULx:URx]

    pts1 = np.float32([[ULx, ULy], [URx, URy], [DLx, DLy], [DRx, DRy]])
    pts2 = np.float32([[0, 0], [500, 0], [0, 500], [500, 500]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(image, M, (500, 500))
    return result


def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # return the warped image
    return warped

if __name__ == '__main__':
        main()
