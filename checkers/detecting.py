
import cv2
import imutils
import numpy as np
from checkers.Field import Field
import requests


class Detector:

    def __init__(self):

        self.url = "http://192.168.1.66:8080/shot.jpg"

        self.STANDARD_DEVIATION = 20
        self.MIN_MATCH_COUNT = 5
        self.FLANN_INDEX_KD_TREE = 0

        self.lower_blue = np.array([110, 100, 50], dtype='uint8')
        self.upper_blue = np.array([130, 255, 255], dtype='uint8')
        self.lower_red1 = np.array([0, 70, 50], dtype='uint8')
        self.upper_red1 = np.array([10, 255, 255], dtype='uint8')
        self.lower_red2 = np.array([170, 70, 50], dtype='uint8')
        self.upper_red2 = np.array([180, 255, 255], dtype='uint8')

    def show_webcam(self, cam, mirror=False):

        while True:
            ret_val, img = cam.read()

    def detect_shape(self, c):
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

    def find_fields(self, image):
        image_black = image.copy()
        image_white = image.copy()

        gray = cv2.cvtColor(image_black, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, 80, 255, cv2.THRESH_BINARY_INV)[1]
        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.erode(thresh, kernel, iterations=1)
        # cv2.imshow("1thresh", thresh)
        # find contours in the thresholded image_black and initialize the
        # shape detector
        cnts1 = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_SIMPLE)
        # contures of black fields
        cnts = imutils.grab_contours(cnts1)

        image_white = cv2.bitwise_not(image_white)
        gray = cv2.cvtColor(image_white, cv2.COLOR_BGR2GRAY)
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

        cnts_sorted = []
        values = []
        for i in range(len(cnts) - 1):
            if i % 2 == 0:
                cnts_sorted.append(cnts[int(i / 2)])
                values.append(Field.BLACK)
            else:
                cnts_sorted.append(cnts[32 + int(i / 2)])
                values.append(Field.WHITE)

        points_of_fields = []
        for c in cnts_sorted:
            shape = self.detect_shape(c)
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
                points_of_fields.append([x, y])
        # cv2.imshow("fields", image)
        return points_of_fields

    def find_pawns(self, image, threshold):

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY)[1]
        # cv2.imshow("pawnsThreshBeforeErode"+str(threshold), thresh)
        # kernel = np.ones((5, 5), np.uint8)
        # thresh = cv2.erode(thresh, kernel, iterations=2)
        # cv2.imshow("pawnsThresh" + str(threshold), thresh)

        # find contours in the thresholded image_black and initialize the
        # shape detector
        cnts1 = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_SIMPLE)
        # contures of black fields
        cnts = imutils.grab_contours(cnts1)

        cnts.reverse()
        # print(str(threshold),len(cnts))

        points_of_pawns = []
        for c in cnts:
            shape = self.detect_shape(c)
            if shape == 'circle':
                x = 0
                y = 0
                count = 0
                for t in c:
                    x = x + t[0][0]
                    y = y + t[0][1]
                    count = count + 1
                x = int(x / count)
                y = int(y / count)
                points_of_pawns.append([x, y])
        #         cv2.circle(image, (x, y), 15, (255, 0, 0), 2)
        #
        # cv2.imshow("circle", image)

        return points_of_pawns

    def check_if_pawn_on_field(self, fields, pawns_blue, pawns_red, image):
        result = []
        for i in range(64):
            if i % 2 == 0:
                result.append(Field.BLACK)
            else:
                result.append(Field.WHITE)

        for id, field in enumerate(fields):
            for pawn in pawns_blue:
                if abs(field[0] - pawn[0]) <= 20 and abs(field[1] - pawn[1]) <= self.STANDARD_DEVIATION:
                    cv2.circle(image, (field[0], field[1]), 10, (255, 0, 255), 3)
                    result[id] = Field.BLACK_FIELD_BLUE_PAWN
                    # print("blue")
            for pawn in pawns_red:
                if abs(field[0] - pawn[0]) <= 20 and abs(field[1] - pawn[1]) <= self.STANDARD_DEVIATION:
                    cv2.circle(image, (field[0], field[1]), 10, (255, 255, 0), 3)
                    result[id] = Field.BLACK_FIELD_RED_PAWN
                    # print("red")

        print(result)

    def find_chessboard(self, image):
        ULx = None
        ULy = None
        URx = None
        URy = None
        DLx = None
        DLy = None
        DRx = None
        DRy = None

        markers_names = ('images/DOWN_LEFT.png', 'images/UP_RIGHT.png', 'images/UP_LEFT.png', 'images/DOWN_RIGHT.png')

        # id is one of the corners of detected image that we need
        img2 = image.copy()  # trainImage
        for id, markerName in enumerate(markers_names):
            img1 = cv2.imread(markerName, 0)  # queryImage



            # Initiate SIFT detector
            sift = cv2.xfeatures2d.SIFT_create()

            # find the keypoints and descriptors with SIFT
            kp1, des1 = sift.detectAndCompute(img1, None)
            kp2, des2 = sift.detectAndCompute(img2, None)

            index_params = dict(algorithm=self.FLANN_INDEX_KD_TREE, trees=5)
            search_params = dict(checks=50)

            flann = cv2.FlannBasedMatcher(index_params, search_params)

            matches = flann.knnMatch(des1, des2, k=2)

            # store all the good matches as per Lowe's ratio test.
            good = []
            for m, n in matches:
                if m.distance < 0.7 * n.distance:
                    good.append(m)

            if len(good) > self.MIN_MATCH_COUNT:
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

    def __main__(self):
        #while True:
            # #img_resp = requests.get(self.url)
            # #img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
            # #img = cv2.imdecode(img_arr, -1)
            #
            # try:
            #     img = self.find_chessboard(img)
            #     # Converts images from BGR to HSV
            #     img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            #     # Find blue pawns
            #     mask = cv2.inRange(img, self.lower_blue, self.upper_blue)
            #     res = cv2.bitwise_and(img, img, mask=mask)
            #     blue_blue_pawns = self.find_pawns(image=res, threshold=50)
            #
            #     # Find red pawns
            #
            #     mask1 = cv2.inRange(img, self.lower_red1, self.upper_red1)
            #
            #     mask2 = cv2.inRange(img, self.lower_red2, self.upper_red2)
            #
            #     res = cv2.bitwise_or(cv2.bitwise_and(img, img, mask=mask1), cv2.bitwise_and(img, img, mask=mask2))
            #     red_pawns = self.find_pawns(image=res, threshold=130)
            #
            #     img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
            #     fields = self.find_fields(img)
            #     self.check_if_pawn_on_field(fields, blue_blue_pawns, red_pawns, img)
            #     cv2.imshow("Wykryte pola", img)
            #     if img is None:
            #         continue
            #     #cv2.imshow("Wykryte pola", img)
            # except:  #?????
            #     continue
            # if cv2.waitKey(1) == 27:
            #     break

        img2 = cv2.imread("images/chessboardARUCO_2.png", 1)
        img = self.find_chessboard(img2)

        # Find blue pawns
        lower_blue = np.array([0, 0, 0], dtype='uint8')
        upper_blue = np.array([255, 50, 50], dtype='uint8')
        mask = cv2.inRange(img, lower_blue, upper_blue)
        res = cv2.bitwise_and(img, img, mask=mask)
        blue_blue_pawns = self.find_pawns(image=res, threshold=30)

        # Find red pawns
        lowerRed = np.array([0, 0, 0], dtype='uint8')
        upperRed = np.array([50, 50, 255], dtype='uint8')
        mask = cv2.inRange(img, lowerRed, upperRed)
        res = cv2.bitwise_and(img, img, mask=mask)
        red_pawns = self.find_pawns(image=res, threshold=50)

        fields = self.find_fields(img)
        self.check_if_pawn_on_field(fields, blue_blue_pawns, red_pawns, img)
        cv2.imshow("Wykryte pola", img)
        cv2.waitKey(0)

        pawns_blue = self.find_pawns(img, 30)
        pawns_red = self.find_pawns(img, 60)
        fields = self.find_fields(img)
        self.check_if_pawn_on_field(fields, pawns_blue, pawns_red, img)
        cv2.imshow("Wykryte pola", img)
        cv2.waitKey(0)

  #  Function to calculate proportion of a certain channel
