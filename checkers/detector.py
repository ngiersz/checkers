import cv2
import imutils
import numpy as np
from Field import Field
import requests
from statistics import mode

STANDARD_DEVIATION = 20


def detect_shape(contours):
    # initialize the shape name and approximate the contour
    shape = None
    peri = 0.04 * cv2.arcLength(contours, True)
    approx = cv2.approxPolyDP(contours, peri, True)
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


def get_fields_as_list_of_points_list(image):

    # finding black fields
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 80, 255, cv2.THRESH_BINARY_INV)[1]
    kernel = np.ones((5, 5), np.uint8)
    dilate = cv2.dilate(thresh, kernel, iterations=6)
    # cv2.imshow("Black fields - dilate", dilate)
    erode = cv2.erode(dilate, kernel, iterations=6)
    # cv2.imshow("Black fields - erode", erode)
    contours_temp = cv2.findContours(erode.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # contours of black fields
    contours = imutils.grab_contours(contours_temp)


    # finding white fields
    image_white = cv2.bitwise_not(image)
    gray = cv2.cvtColor(image_white, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY_INV)[1]
    kernel = np.ones((5, 5), np.uint8)
    erode = cv2.erode(thresh, kernel, iterations=6)
    # cv2.imshow("White fields - erode", erode)
    dilate = cv2.dilate(erode, kernel, iterations=6)
    # cv2.imshow("Black fields - dilate", dilate)
    contours_temp = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # add contours of white fields
    contours = imutils.grab_contours(contours_temp) + contours
    contours.reverse()
    # check if 64 fields are detected
    if len(contours) != 64:
        return None

    contours_sorted = []
    values_of_fields = []
    for i in range(len(contours)):
        if i % 2 == 0:
            contours_sorted.append(contours[int(i/2)])
            values_of_fields.append(Field.BLACK)
        else:
            contours_sorted.append(contours[32 + int(i/2)])
            values_of_fields.append(Field.WHITE)

    list_of_points_list = []
    list_of_points_in_one_row = []
    for i, c in enumerate(contours_sorted):
        shape = detect_shape(c)
        if shape == 'square':
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            x = 0
            y = 0
            count = 0
            for one_measurement in c:
                x = x + one_measurement[0][0] # x of measurement
                y = y + one_measurement[0][1] # y of measurement
                count = count + 1 # count of measurements

            x = int(x / count) # x mean of measurements
            y = int(y / count) # y mean of measurements
            list_of_points_in_one_row.append([x,y])

        if len(list_of_points_in_one_row) == 8:
            list_of_points_in_one_row.sort(key=lambda x: x[0])
            list_of_points_list = list_of_points_list + list_of_points_in_one_row
            list_of_points_in_one_row =[]

    for i in range(len(list_of_points_list)):
        cv2.putText(image, str(i),(list_of_points_list[i][0], list_of_points_list[i][1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (127,127,127),2, cv2.LINE_AA )

    return list_of_points_list #, image


def get_list_of_pawns_points(image, threshold):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY)[1]
    # cv2.imshow("pawnsThreshBeforeErode"+str(threshold), thresh)
    kernel = np.ones((5, 5), np.uint8)
    erode = cv2.erode(thresh, kernel, iterations=2)
    # cv2.imshow("pawnsThresh" + str(threshold) + 'erode', erode)
    dilate = cv2.dilate(erode, kernel, iterations=3)
    # cv2.imshow("pawnsThresh" + str(threshold) + 'dilate', dilate)


    contours_temp = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    # contours of black fields
    contours = imutils.grab_contours(contours_temp)
    contours.reverse()
    list_of_pawns_points = []
    for c in contours:
        shape = detect_shape(c)
        # if shape == 'circle':
        x = 0
        y = 0
        count = 0
        for t in c:
            x = x + t[0][0]
            y = y + t[0][1]
            count = count + 1
        x = int(x/count)
        y = int(y/count)
        list_of_pawns_points.append([x, y])

    return list_of_pawns_points


def get_fields_info_as_list(list_of_fields_points, list_of_blue_pawns_points, list_of_red_pawns_points, image):
    # initialize list with empty black and white fields
    result = []
    for i in range(64):
        if i % 2 == 0:
            result.append(Field.BLACK)
        else:
            result.append(Field.WHITE)

    for id, field in enumerate(list_of_fields_points):
        for pawn in list_of_blue_pawns_points:
            if abs(field[0] - pawn[0]) <= 20 and abs(field[1] - pawn[1]) <= STANDARD_DEVIATION:
                cv2.circle(image, (field[0], field[1]), 10, (255, 0, 255), 3)
                result[id] = Field.BLACK_FIELD_BLUE_PAWN
                # print("blue")
        for pawn in list_of_red_pawns_points:
            if abs(field[0] - pawn[0]) <= 20 and abs(field[1] - pawn[1]) <= STANDARD_DEVIATION:
                cv2.circle(image, (field[0], field[1]), 10, (255, 255, 0), 3)
                result[id] = Field.BLACK_FIELD_RED_PAWN
                # print("red")

    return result


def get_chessboard_as_image(image):
    ULx = None  # x of UP LEFT corner
    ULy = None  # y of UP LEFT corner
    URx = None  # x of UP RIGHT corner
    URy = None  # y of UP RIGHT corner
    DLx = None  # x of DOWN LEFT corner
    DLy = None  # y of DOWN LEFT corner
    DRx = None  # x of DOWN RIGHT corner
    DRy = None  # y of DOWN RIGHT corner

    MIN_MATCH_COUNT = 5
    FLANN_INDEX_KDTREE = 0

    markers_names = ('images/DOWN_LEFT.png', 'images/UP_RIGHT.png', 'images/UP_LEFT.png', 'images/DOWN_RIGHT.png')

    # id is one of the corners of detected image that we need
    train_image = image.copy()
    for id, markerName in enumerate(markers_names):
        query_image = cv2.imread(markerName, 0)

        # Initiate SIFT detector
        sift = cv2.xfeatures2d.SIFT_create()

        # find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(query_image, None)
        kp2, des2 = sift.detectAndCompute(train_image, None)

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
            h, w = query_image.shape
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


def start(camera_image):
    url = "http://192.168.1.66:8080/shot.jpg"
    n = 5
    n_results = [[] for i in range(64)]
    while True:
        counter = 0
        while counter < n:
            img_resp = requests.get(url)
            img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
            camera_image = cv2.imdecode(img_arr, -1)

            try:
                image = get_chessboard_as_image(camera_image)
                # Converts images from BGR to HSV
                image_HSV = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2HSV)

                # Find blue pawns
                lower_blue = np.array([100, 100, 50], dtype='uint8')
                upper_blue = np.array([130, 255, 255], dtype='uint8')
                mask = cv2.inRange(image_HSV, lower_blue, upper_blue)
                res = cv2.bitwise_and(image_HSV, image_HSV, mask=mask)
                blue_pawns = get_list_of_pawns_points(image=res, threshold=100)

                # Find red pawns
                lower_red1 = np.array([0, 70, 50], dtype='uint8')
                upper_red1 = np.array([10, 255, 255], dtype='uint8')
                mask1 = cv2.inRange(image_HSV, lower_red1, upper_red1)
                lower_red2 = np.array([170, 70, 50], dtype='uint8')
                upper_red2 = np.array([180, 255, 255], dtype='uint8')
                mask2 = cv2.inRange(image_HSV, lower_red2, upper_red2)
                res = cv2.bitwise_or(cv2.bitwise_and(image_HSV, image_HSV, mask=mask1), cv2.bitwise_and(image_HSV, image_HSV, mask=mask2))
                red_pawns = get_list_of_pawns_points(image=res, threshold=130)

                # Find fields
                fields = get_fields_as_list_of_points_list(image)

                info_about_each_field = get_fields_info_as_list(fields, blue_pawns, red_pawns, image)
                for i, x in enumerate(info_about_each_field):
                    n_results[i].append(x)

                if image is None:
                    counter = counter - 1
                    continue
                counter = counter + 1

                cv2.imshow("Wykryte pola", image)

            except:
                continue
            if cv2.waitKey(1) == 27:
                break
        result = []
        for each_field in n_results:
            result.append(mode(each_field))


        # show pretty table result :)
        for i, x in enumerate(result):
            if i % 8 == 0:
                print("")
            if x == Field.BLACK_FIELD_BLUE_PAWN:
                print(1, end='')
            elif x == Field.BLACK_FIELD_RED_PAWN:
                print(2, end='')
            else:
                print(0, end='')
        print("")

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
    #
    # pawnsBlue = findPawns(img, 30)
    # pawnsRed = findPawns(img, 60)
    # fields = findFields(img)
    # checkIfPawnOnField(fields, pawnsBlue, pawnsRed, img)
    # cv2.imshow("Wykryte pola", img)
    # cv2.waitKey(0)


if __name__ == '__main__':
    start(None)