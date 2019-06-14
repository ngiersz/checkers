import cv2
import imutils
import numpy as np
from checkers.fields import Field
from checkers.fields import Player
import requests
from statistics import mode
from cv2 import aruco
import operator
ERROR_LIMIT = 30


def detect_shape(contour):
    shape = None
    approx = cv2.approxPolyDP(contour, 0.1 * cv2.arcLength(contour, True), True)

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
    black_contours = imutils.grab_contours(contours_temp)

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
    # contours of white fields
    white_contours = imutils.grab_contours(contours_temp)
    # add contours of white fields
    contours = black_contours + white_contours
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

    return list_of_points_list  # , image


def get_list_of_pawns_points(image):
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    thresh = cv2.threshold(blurred, 130, 255, cv2.THRESH_BINARY)[1]

    contours_temp, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours_temp.reverse()
    list_of_pawns_points = []
    list_of_queens_points = []
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
            y = int(int(y / count))
            list_of_queens_points.append([x, y])
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

    return list_of_pawns_points, list_of_queens_points


def get_fields_info_as_list_of_lists(list_of_fields_points, list_of_blue_pawns_points, list_of_blue_queens_points,
                                     list_of_red_pawns_points, list_of_red_queens_points, image):
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
            if abs(field[0] - pawn[0]) <= ERROR_LIMIT and abs(field[1] - pawn[1]) <= ERROR_LIMIT:
                cv2.circle(image, (field[0], field[1]), 10, (0, 0, 255), 3)
                result[id] = Field.BLACK_FIELD_BLUE_PAWN
                break

        for pawn in list_of_blue_queens_points:
            if abs(field[0] - pawn[0]) <= ERROR_LIMIT and abs(field[1] - pawn[1]) <= ERROR_LIMIT:
                cv2.circle(image, (field[0], field[1]), 10, (0, 0, 127), 3)
                result[id] = Field.BLACK_FIELD_BLUE_QUEEN
                break

        for pawn in list_of_red_pawns_points:
            if abs(field[0] - pawn[0]) <= ERROR_LIMIT and abs(field[1] - pawn[1]) <= ERROR_LIMIT:
                cv2.circle(image, (field[0], field[1]), 10, (255, 0, 0), 3)
                result[id] = Field.BLACK_FIELD_RED_PAWN
                break

        for pawn in list_of_red_queens_points:
            if abs(field[0] - pawn[0]) <= ERROR_LIMIT and abs(field[1] - pawn[1]) <= ERROR_LIMIT:
                cv2.circle(image, (field[0], field[1]), 10, (127, 0, 0), 3)
                result[id] = Field.BLACK_FIELD_RED_QUEEN
                break

    final_result = []
    temp_result = []

    for i, each_field in enumerate(result):
        if i % 8 == 0 and i != 0:
            final_result.append(temp_result)
            temp_result = []
        temp_result.append(each_field)

    final_result.append(temp_result)

    return final_result


def get_chessboard_as_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41, 40)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_7X7_50)
    parameters = aruco.DetectorParameters_create()
    corners, ids, _ = aruco.detectMarkers(thresh, aruco_dict, parameters=parameters)

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


def detect(camera_image, last_result):
    try:
        image = get_chessboard_as_image(camera_image)
        imgScale = 2.5
        newX, newY = image.shape[1] * imgScale, image.shape[0] * imgScale
        image_resized = cv2.resize(image, (int(newX), int(newY)))
        # Converts images from BGR to HSV
        image_HSV = cv2.cvtColor(image_resized.copy(), cv2.COLOR_BGR2HSV)

        # Find blue pawns
        lower_blue = np.array([60, 95, 120])  # 20-90, 70-120, 100-140
        upper_blue = np.array([145, 255, 255])  # 120-170
        blue_mask = cv2.inRange(image_HSV, lower_blue, upper_blue)
        kernel = np.ones((5, 5), np.uint8)
        blue_mask = cv2.erode(blue_mask, kernel, iterations=1)
        blue_mask = cv2.dilate(blue_mask, kernel, iterations=2)
        imgScale = 0.4
        newX, newY = blue_mask.shape[1] * imgScale, blue_mask.shape[0] * imgScale
        blue_mask = cv2.resize(blue_mask, (int(newX), int(newY)))
        blue_pawns, blue_queens = get_list_of_pawns_points(image=blue_mask)

        # Find red pawns
        lower_red_and_blue = np.array([0, 120, 130])
        upper_red_and_blue = np.array([180, 255, 255])
        red_and_blue_mask = cv2.inRange(image_HSV, lower_red_and_blue, upper_red_and_blue)
        kernel = np.ones((5, 5), np.uint8)

        red_and_blue_mask = cv2.erode(red_and_blue_mask, kernel, iterations=1)
        red_and_blue_mask = cv2.dilate(red_and_blue_mask, kernel, iterations=2)

        imgScale = 0.4
        newX, newY = red_and_blue_mask.shape[1] * imgScale, red_and_blue_mask.shape[0] * imgScale
        red_and_blue_mask = cv2.resize(red_and_blue_mask, (int(newX), int(newY)))
        red_mask = cv2.bitwise_and(red_and_blue_mask, cv2.bitwise_not(blue_mask))
        red_pawns, red_queens = get_list_of_pawns_points(image=red_mask)

        # Find fields
        fields = get_fields_as_list_of_points_list(image)


        info_about_each_field = get_fields_info_as_list_of_lists(list_of_fields_points=fields, image=image,
                                                                 list_of_blue_pawns_points=blue_pawns,
                                                                 list_of_blue_queens_points=blue_queens,
                                                                 list_of_red_pawns_points=red_pawns,
                                                                 list_of_red_queens_points=red_queens)

    except Exception as e:
        print("exception: " + str(e))
        return camera_image, last_result


    return image, info_about_each_field


def startTest():
    url = "http://192.168.1.66:8080/shot.jpg"
    n_results = [[] for i in range(64)]
    counter = 0
    number_of_fails = 0
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    camera_image = cv2.imdecode(img_arr, -1)
    while True:

        image = get_chessboard_as_image(camera_image)
        # Converts images from BGR to HSV
        imgScale = 2.5
        newX, newY = image.shape[1] * imgScale, image.shape[0] * imgScale
        image_resized = cv2.resize(image, (int(newX), int(newY)))
        image_HSV = cv2.cvtColor(image_resized.copy(), cv2.COLOR_BGR2HSV)


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
        imgScale = 0.4
        newX, newY = blue_mask.shape[1] * imgScale, blue_mask.shape[0] * imgScale
        blue_mask = cv2.resize(blue_mask, (int(newX), int(newY)))
        blue_pawns, blue_queens = get_list_of_pawns_points(image=blue_mask, threshold=131)

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
        imgScale = 0.4
        newX, newY = red_and_blue_mask.shape[1] * imgScale, red_and_blue_mask.shape[0] * imgScale
        red_and_blue_mask = cv2.resize(red_and_blue_mask, (int(newX), int(newY)))
        red_mask = cv2.bitwise_and(red_and_blue_mask, cv2.bitwise_not(blue_mask))
        red_pawns, red_queens = get_list_of_pawns_points(image=red_mask, threshold=100)

        # Find fields
        fields = get_fields_as_list_of_points_list(image)
        if fields is None:
            number_of_fails += 1
            continue


        info_about_each_field = get_fields_info_as_list_of_lists(list_of_fields_points=fields, image=image,
                                                                 list_of_blue_pawns_points=blue_pawns,
                                                                 list_of_blue_queens_points=blue_queens,
                                                                 list_of_red_pawns_points=red_pawns,
                                                                 list_of_red_queens_points=red_queens)
        cv2.imshow("Wykryte pionki", image)
        cv2.waitKey(1)

        for i, x in enumerate(info_about_each_field):
            n_results[i].append(x)

        if image is None:
            counter = counter - 1
            number_of_fails += 1
            continue
        counter = counter + 1



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
    # for x in result:
    #     for y in x:
    #         print(y.value, end=';')
    #     print('')
    print("result---------------------------------------")
    print(result)


if __name__ == '__main__':
    startTest()
