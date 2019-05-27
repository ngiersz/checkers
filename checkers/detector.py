import cv2
import imutils
import numpy as np
from checkers.Field import Field
import requests
from statistics import mode
from cv2 import aruco
import operator
STANDARD_DEVIATION = 30

def detect_shape(contours):
    # # initialize the shape name and approximate the contour
    # shape = None
    # peri = 0.04 * cv2.arcLength(contours, True)
    # approx = cv2.approxPolyDP(contours, peri, True)
    # # if the shape has 4 vertices, it is either a square or
    # # a rectangle
    # if len(approx) == 4:
    #     # a square will have an aspect ratio that is approximately
    #     # equal to one, otherwise, the shape is a rectangle
    #     shape = "square"  # if ar >= 0.95 and ar <= 1.05 else "rectangle"
    # elif len(approx) == 3:
    #     shape = "triangle"
    # # # otherwise, we assume the shape is a circle
    # else:
    #     shape = "circle"

    shape = None
    area = cv2.contourArea(contours)
    approx = cv2.approxPolyDP(contours, 0.1 * cv2.arcLength(contours, True), True)

    # if area > 200:
    if len(approx) == 4:
        shape = 'square'
    elif len(approx) == 3:
        shape = 'triangle'
    else:
        shape = 'circle'

    # return the name of the shape
    return shape


def get_fields_as_list_of_points_list(image):
    # find black fields
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY_INV)[1]
    # cv2.imshow("Black fields - thresh", thresh)
    kernel = np.ones((5, 5), np.uint8)
    dilate = cv2.dilate(thresh, kernel, iterations=6)
    # cv2.imshow("Black fields - dilate", dilate)
    erode = cv2.erode(dilate, kernel, iterations=7)
    # cv2.imshow("Black fields - erode", erode)
    contours_temp = cv2.findContours(erode.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # contours of black fields
    contours = imutils.grab_contours(contours_temp)

    # find white fields
    image_white = cv2.bitwise_not(image)
    gray = cv2.cvtColor(image_white, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY_INV)[1]
    kernel = np.ones((5, 5), np.uint8)
    erode = cv2.erode(thresh, kernel, iterations=7)
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
    for i in range(len(contours)):
        if i % 2 == 0:
            contours_sorted.append(contours[int(i / 2)])
        else:
            contours_sorted.append(contours[32 + int(i / 2)])

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
                x = x + one_measurement[0][0]  # x of measurement
                y = y + one_measurement[0][1]  # y of measurement
                count = count + 1  # count of measurements

            x = int(x / count)  # x mean of measurements
            y = int(y / count)  # y mean of measurements
            list_of_points_in_one_row.append([x, y])

        if len(list_of_points_in_one_row) == 8:
            list_of_points_in_one_row.sort(key=lambda x: x[0])
            list_of_points_list = list_of_points_list + list_of_points_in_one_row
            list_of_points_in_one_row = []

    # draw number of field
    # for i in range(len(list_of_points_list)):
    #     cv2.putText(image, str(i), (list_of_points_list[i][0], list_of_points_list[i][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (127, 127, 127), 2 , cv2.LINE_AA)
    # print(len(list_of_points_list[5]))
    return list_of_points_list  # , image


def get_list_of_pawns_points(image, threshold):
    imgScale = 0.4
    newX, newY = image.shape[1] * imgScale, image.shape[0] * imgScale
    image_resized = cv2.resize(image, (int(newX), int(newY)))
    # cv2.imshow("pawnsThreshBeforeErode"+str(threshold), image_resized)
    # cv2.waitKey(1)
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(image_resized, (5, 5), 0)
    thresh = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY)[1]

    contours_temp, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours_temp.reverse()
    list_of_pawns_points = []
    list_of_kings_points = []
    for c in contours_temp:
        shape = detect_shape(c)
        if shape == 'triangle':
            x = 0
            y = 0
            count = 0
            for t in c:
                x = x + t[0][0]
                y = y + t[0][1]
                count = count + 1
            x = int(int(x / count))
            y = int(int(y / count) )
            list_of_kings_points.append([x, y])
        else:
            x = 0
            y = 0
            count = 0
            for t in c:
                x = x + t[0][0]
                y = y + t[0][1]
                count = count + 1
            x = int(int(x / count))
            y = int(int(y / count))
            list_of_pawns_points.append([x, y])

    return list_of_pawns_points, list_of_kings_points


def get_fields_info_as_list(list_of_fields_points, list_of_blue_pawns_points, list_of_blue_kings_points,
                            list_of_red_pawns_points, list_of_red_kings_points, image):
    # initialize list with empty black and white fields
    result = []
    counter = 0
    for i in range(64):
        if (i + int(counter / 8)) % 2 == 0:
            result.append(Field.BLACK)
        else:
            result.append(Field.WHITE)
        counter += 1

    for id, field in enumerate(list_of_fields_points):
        for pawn in list_of_blue_pawns_points:
            if abs(field[0] - pawn[0]) <= 20 and abs(field[1] - pawn[1]) <= STANDARD_DEVIATION:
                cv2.circle(image, (field[0], field[1]), 10, (0, 0, 255), 3)
                result[id] = Field.BLACK_FIELD_BLUE_PAWN

        for pawn in list_of_blue_kings_points:
            if abs(field[0] - pawn[0]) <= 20 and abs(field[1] - pawn[1]) <= STANDARD_DEVIATION:
                cv2.circle(image, (field[0], field[1]), 10, (0, 0, 127), 3)
                result[id] = Field.BLACK_FIELD_BLUE_KING

        for pawn in list_of_red_pawns_points:
            if abs(field[0] - pawn[0]) <= 20 and abs(field[1] - pawn[1]) <= STANDARD_DEVIATION:
                cv2.circle(image, (field[0], field[1]), 10, (255, 0, 0), 3)
                result[id] = Field.BLACK_FIELD_RED_PAWN

        for pawn in list_of_red_kings_points:
            if abs(field[0] - pawn[0]) <= 20 and abs(field[1] - pawn[1]) <= STANDARD_DEVIATION:
                cv2.circle(image, (field[0], field[1]), 10, (127, 0, 0), 3)
                result[id] = Field.BLACK_FIELD_RED_KING

    return result


def get_chessboard_as_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41, 40)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_7X7_50)
    parameters = aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(thresh, aruco_dict, parameters=parameters)
    frame_markers = aruco.drawDetectedMarkers(image.copy(), corners, ids)

    # print(tuple(rejectedImgPoints[0][0][0]))
    # for x in rejectedImgPoints:
    #     cv2.circle(image,tuple(x[0][0]),8, (255,0,0), 8)
    # cv2.imshow("aa", frame_markers)
    # cv2.waitKey(0)

    if len(corners) < 4:
        return None
    sorted_corners = [x for _, x in sorted(zip(ids, corners))]

    ULx = sorted_corners[0][0][2][0]  # x of UP LEFT corner
    ULy = sorted_corners[0][0][2][1]  # y of UP LEFT corner
    URx = sorted_corners[3][0][3][0]  # x of UP RIGHT corner
    URy = sorted_corners[3][0][3][1]  # y of UP RIGHT corner
    DLx = sorted_corners[2][0][1][0]  # x of DOWN LEFT corner
    DLy = sorted_corners[2][0][1][1]  # y of DOWN LEFT corner
    DRx = sorted_corners[1][0][0][0]  # x of DOWN RIGHT corner
    DRy = sorted_corners[1][0][0][1]  # y of DOWN RIGHT corner

    pts1 = np.float32([[ULx, ULy], [URx, URy], [DLx, DLy], [DRx, DRy]])
    pts2 = np.float32([[0, 0], [500, 0], [0, 500], [500, 500]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(image, M, (500, 500))
    return result

#
#
# def nothing(x):
#     # any operation
#     pass


# cv2.namedWindow("Trackbars")
# cv2.createTrackbar("L-H", "Trackbars", 0, 180, nothing)
# cv2.createTrackbar("L-S", "Trackbars", 66, 255, nothing)
# cv2.createTrackbar("L-V", "Trackbars", 134, 255, nothing)
# cv2.createTrackbar("U-H", "Trackbars", 180, 180, nothing)
# cv2.createTrackbar("U-S", "Trackbars", 255, 255, nothing)
# cv2.createTrackbar("U-V", "Trackbars", 243, 255, nothing)


def start(camera_image, last_result, n=5):
    n_results = [[] for i in range(64)]
    counter = 0
    number_of_fails = 0
    while counter < n:

        if number_of_fails > 10:
            return camera_image, last_result

        try:
            image = get_chessboard_as_image(camera_image)

            # Converts images from BGR to HSV
            imgScale = 2.5
            newX, newY = image.shape[1] * imgScale, image.shape[0] * imgScale
            image_resized = cv2.resize(image, (int(newX), int(newY)))
            image_HSV = cv2.cvtColor(image_resized.copy(), cv2.COLOR_BGR2HSV)


            l_h = cv2.getTrackbarPos("L-H", "Trackbars")
            l_s = cv2.getTrackbarPos("L-S", "Trackbars")
            l_v = cv2.getTrackbarPos("L-V", "Trackbars")
            u_h = cv2.getTrackbarPos("U-H", "Trackbars")
            u_s = cv2.getTrackbarPos("U-S", "Trackbars")
            u_v = cv2.getTrackbarPos("U-V", "Trackbars")
            # lower_blue = np.array([l_h, l_s, l_v])
            # upper_blue = np.array([u_h, u_s, u_v])

            # Find blue pawns
            # lower_blue = np.array([30, 90, 110])
            # upper_blue = np.array([130, 255, 255])
            # noc
            # lower_blue = np.array([40, 40, 120])
            # upper_blue = np.array([150, 255, 255])
            # dzien
            lower_blue = np.array([60, 95, 120]) #20-90, 70-120, 100-140
            upper_blue = np.array([145, 255, 255]) #120-170
            # lower_blue = np.array([l_h, l_s, l_v])
            # upper_blue = np.array([u_h, u_s, u_v])
            blue_mask = cv2.inRange(image_HSV, lower_blue, upper_blue)
            kernel = np.ones((5, 5), np.uint8)
            # cv2.imshow("blue przed", blue_mask)
            # cv2.waitKey(1)
            blue_mask = cv2.erode(blue_mask, kernel, iterations=1)
            blue_mask = cv2.dilate(blue_mask, kernel, iterations=2)
            # cv2.imshow("blue po", blue_mask)
            # cv2.waitKey(1)
            blue_pawns, blue_kings = get_list_of_pawns_points(image=blue_mask, threshold=131)

            # # Find red pawns
            lower_red = np.array([0, 100, 130])
            upper_red = np.array([180, 255, 255])
            # lower_red = np.array([l_h, l_s, l_v])
            # upper_red = np.array([u_h, u_s, u_v])
            red_and_blue_mask = cv2.inRange(image_HSV, lower_red, upper_red)
            kernel = np.ones((5, 5), np.uint8)
            # cv2.imshow("red przed", red_and_blue_mask)
            # cv2.waitKey(1)
            red_and_blue_mask = cv2.erode(red_and_blue_mask, kernel, iterations=1)
            red_and_blue_mask = cv2.dilate(red_and_blue_mask, kernel, iterations=2)
            # cv2.imshow("red po", red_and_blue_mask)
            # cv2.waitKey(1)
            red_mask = cv2.bitwise_and(red_and_blue_mask, cv2.bitwise_not(blue_mask))
            red_pawns, red_kings = get_list_of_pawns_points(image=red_mask, threshold=100)

            # Find fields
            fields = get_fields_as_list_of_points_list(image)
            if fields is None:
                number_of_fails += 1
                continue

            info_about_each_field = get_fields_info_as_list(list_of_fields_points=fields, image=image,
                                                            list_of_blue_pawns_points=blue_pawns,
                                                            list_of_blue_kings_points=blue_kings,
                                                            list_of_red_pawns_points=red_pawns,
                                                            list_of_red_kings_points=red_kings)
            #
            # cv2.imshow("plansza", image)
            # cv2.waitKey(1)
            for i, x in enumerate(info_about_each_field):
                n_results[i].append(x)

            if image is None:
                counter = counter - 1
                number_of_fails += 1
                continue
            counter = counter + 1

        except Exception as e:
            number_of_fails += 1
            continue

        if cv2.waitKey(1) == 27:
            break

    result = []
    temp_result = []

    for i, each_field in enumerate(n_results):
        if i % 8 == 0 and i != 0:
            result.append(temp_result)
            temp_result = []
        try:
            temp_result.append(mode(each_field))
        except:
            unique_values = set(each_field)
            value_count_dict = dict.fromkeys(unique_values, 0)
            for value in each_field:
                value_count_dict[value] += 1
            temp_result.append(max(value_count_dict.items(), key=operator.itemgetter(1))[0])

    result.append(temp_result)

    # check result
    for x in result:
        for y in x:
            print(y, end='; ')
        print('\n')

    return image, result


def startTest():
    url = "http://192.168.1.66:8080/shot.jpg"
    n = 5
    n_results = [[] for i in range(64)]
    while True:
        counter = 0
        while counter < n:
            img_resp = requests.get(url)
            img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
            camera_image = cv2.imdecode(img_arr, -1)

            image = get_chessboard_as_image(camera_image)
            while image is None:
                img_resp = requests.get(url)
                img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
                camera_image = cv2.imdecode(img_arr, -1)
                image = get_chessboard_as_image(camera_image)

            # Converts images from BGR to HSV
            image_HSV = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2HSV)

            # Find blue pawns v1
            # lower_blue = np.array([100, 100, 50], dtype='uint8')
            # upper_blue = np.array([130, 255, 255], dtype='uint8')
            # mask = cv2.inRange(image_HSV, lower_blue, upper_blue)
            # res = cv2.bitwise_and(image_HSV, image_HSV, mask=mask)
            # blue_pawns = get_list_of_pawns_points(image=res, threshold=131)

            # Find blue pawns v2
            lower_blue = np.array([150, 0, 0], dtype='uint8')
            upper_blue = np.array([255, 255, 255], dtype='uint8')
            mask = cv2.inRange(image, lower_blue, upper_blue)
            res = cv2.bitwise_and(image_HSV, image_HSV, mask=mask)
            blue_pawns = get_list_of_pawns_points(image=res, threshold=200)


            # Find red pawns
            lower_red1 = np.array([0, 70, 50], dtype='uint8')
            upper_red1 = np.array([10, 255, 255], dtype='uint8')
            mask1 = cv2.inRange(image_HSV, lower_red1, upper_red1)
            lower_red2 = np.array([150, 70, 50], dtype='uint8')
            upper_red2 = np.array([180, 255, 255], dtype='uint8')
            mask2 = cv2.inRange(image_HSV, lower_red2, upper_red2)
            res = cv2.bitwise_or(cv2.bitwise_and(image_HSV, image_HSV, mask=mask1),
                                 cv2.bitwise_and(image_HSV, image_HSV, mask=mask2))

            red_pawns = get_list_of_pawns_points(image=res, threshold=130)

            # lower_red = np.array([0, 0, 100], dtype='uint8')
            # upper_red = np.array([255, 255, 255], dtype='uint8')
            # mask = cv2.inRange(image, lower_red, upper_red)
            # res = cv2.bitwise_and(image_HSV, image_HSV, mask=mask)
            # cv2.imshow("red", res)
            # red_pawns = get_list_of_pawns_points(image=res, threshold=170)

            # Find fields
            fields = get_fields_as_list_of_points_list(image)
            if fields is None:
                continue

            info_about_each_field = get_fields_info_as_list(fields, blue_pawns, red_pawns, image)
            for i, x in enumerate(info_about_each_field):
                n_results[i].append(x)

            if image is None:
                counter = counter - 1
                continue
            counter = counter + 1

            cv2.imshow("Wykryte pola", image)

            if cv2.waitKey(1) == 27:
                break

        result = []
        for each_field in n_results:
            result.append(mode(each_field))

        # # show pretty table result :)
        # for i, x in enumerate(result):
        #     if i % 8 == 0:
        #         print("")
        #     if x == Field.BLACK_FIELD_BLUE_PAWN:
        #         print(1, end='')
        #     elif x == Field.BLACK_FIELD_RED_PAWN:
        #         print(2, end='')
        #     else:
        #         print(0, end='')
        # print("")


if __name__ == '__main__':
    startTest()
