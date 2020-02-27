# -*- coding: UTF-8 -*-

import cv2
import numpy as np
import math
import time


def avg_circles(circles, b):
    avg_x = 0
    avg_y = 0
    avg_r = 0
    for i in range(b):
        # optional - average for multiple circles (can happen when a dashboard is at a slight angle)
        avg_x = avg_x + circles[0][i][0]
        avg_y = avg_y + circles[0][i][1]
        avg_r = avg_r + circles[0][i][2]
    avg_x = int(avg_x / (b))
    avg_y = int(avg_y / (b))
    avg_r = int(avg_r / (b))
    return avg_x, avg_y, avg_r


def dist_2_pts(x1, y1, x2, y2):
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def calibrate(img):
    '''
    This function should be run using a test image in order to calibrate the range available to the dial as well as the
    units.  It works by first finding the center point and radius of the dashboard.  Then it draws lines at hard coded intervals
    (separation) in degrees.  It then prompts the user to enter position in degrees of the lowest possible value of the dashboard,
    as well as the starting value (which is probably zero in most cases but it won't assume that).  It will then ask for the
    position in degrees of the largest possible value of the dashboard. Finally, it will ask for the units.  This assumes that
    the dashboard is linear (as most probably are).
    It will return the min value with angle in degrees (as a tuple), the max value with angle in degrees (as a tuple),
    and the units (as a string).
    '''

    height, width = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to gray
    # gray = cv2.GaussianBlur(gray, (5, 5), 0)
    # gray = cv2.medianBlur(gray, 5)

    # for testing, output gray image
    # cv2.imwrite('./out/%s-bw.%s' %(0, 'jpg'),gray)

    # detect circles
    # restricting the search from 35-48% of the possible radii gives fairly good results across different samples.  Remember that
    # these are pixel values which correspond to the possible radii search range.
    # 霍夫圆环检测
    # image:8位, 单通道图像
    # method：定义检测图像中圆的方法. 目前唯一实现的方法cv2.HOUGH_GRADIENT.

    # dp：累加器分辨率与图像分辨率的反比. dp获取越大, 累加器数组越小.
    # minDist：检测到的圆的中心,  (x,y) 坐标之间的最小距离. 如果minDist太小, 则可能导致检测到多个相邻的圆. 如果minDist太大, 则可能导致很多圆检测不到.
    # param1：用于处理边缘检测的梯度值方法.
    # param2：cv2.HOUGH_GRADIENT方法的累加器阈值. 阈值越小, 检测到的圈子越多.
    # minRadius：半径的最小大小 (以像素为单位).
    # maxRadius：半径的最大大小 (以像素为单位).

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, np.array([]),
                               100, 50, int(height * 0.35), int(height * 0.48))
    # average found circles, found it to be more accurate than trying to tune HoughCircles parameters to get just the right one
    a, b, c = circles.shape
    #获取圆的坐标x,y和半径r
    x, y, r = avg_circles(circles, b)

    return x, y, r


def draw_calibration(img, x, y, r):
    # draw center and circle
    cv2.circle(img, (x, y), r, (0, 0, 255), 3, cv2.LINE_AA)  # draw circle
    cv2.circle(img, (x, y), 2, (0, 255, 0), 3,
               cv2.LINE_AA)  # draw center of circle

    # for calibration, plot lines from center going out at every 10 degrees and add marker

    separation = 10.0  # in degrees
    interval = int(360 / separation)
    p1 = np.zeros((interval, 2))  # set empty arrays
    p2 = np.zeros((interval, 2))
    p_text = np.zeros((interval, 2))
    for i in range(0, interval):
        for j in range(0, 2):
            if (j % 2 == 0):
                p1[i][j] = x + 0.5 * r * np.cos(
                    separation * i * math.pi / 180)  # point for lines
            else:
                p1[i][j] = y + 0.5 * r * np.sin(separation * i * math.pi / 180)
    text_offset_x = 10
    text_offset_y = 5
    for i in range(0, interval):
        for j in range(0, 2):
            if (j % 2 == 0):
                p2[i][j] = x + r * np.cos(separation * i * math.pi / 180)
                p_text[i][j] = x - text_offset_x + 1.1 * r * np.cos(
                    (separation) * (i + 9) * math.pi / 180
                )  # point for text labels, i+9 rotates the labels by 90 degrees
            else:
                p2[i][j] = y + r * np.sin(separation * i * math.pi / 180)
                p_text[i][j] = y + text_offset_y + 1.1 * r * np.sin(
                    (separation) * (i + 9) * math.pi / 180
                )  # point for text labels, i+9 rotates the labels by 90 degrees

    # add the lines and labels to the image
    for i in range(0, interval):
        cv2.line(img, (int(p1[i][0]), int(p1[i][1])),
                 (int(p2[i][0]), int(p2[i][1])), (0, 255, 0), 2)
        cv2.putText(img, '%s' % (int(i * separation)),
                    (int(p_text[i][0]), int(p_text[i][1])),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
    return img


def get_current_value(img, min_angle, max_angle, min_value, max_value, x, y,
                      r):

    gray2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Set threshold and maxValue
    thresh = 175
    maxValue = 255

    # for testing purposes, found cv2.THRESH_BINARY_INV to perform the best
    # th, dst1 = cv2.threshold(gray2, thresh, maxValue, cv2.THRESH_BINARY);
    # th, dst2 = cv2.threshold(gray2, thresh, maxValue, cv2.THRESH_BINARY_INV);
    # th, dst3 = cv2.threshold(gray2, thresh, maxValue, cv2.THRESH_TRUNC);
    # th, dst4 = cv2.threshold(gray2, thresh, maxValue, cv2.THRESH_TOZERO);
    # th, dst5 = cv2.threshold(gray2, thresh, maxValue, cv2.THRESH_TOZERO_INV);
    # cv2.imwrite('./out/%s-dst1.%s' % (0, 'jpg'), dst1)
    # cv2.imwrite('./out/%s-dst2.%s' % (0, 'jpg'), dst2)
    # cv2.imwrite('./out/%s-dst3.%s' % (0, 'jpg'), dst3)
    # cv2.imwrite('./out/%s-dst4.%s' % (0, 'jpg'), dst4)
    # cv2.imwrite('./out/%s-dst5.%s' % (0, 'jpg'), dst5)

    # apply thresholding which helps for finding lines
    th, dst2 = cv2.threshold(gray2, thresh, maxValue, cv2.THRESH_BINARY_INV)

    # found Hough Lines generally performs better without Canny / blurring, though there were a couple exceptions where it would only work with Canny / blurring
    dst2 = cv2.medianBlur(dst2, 5)
    dst2 = cv2.Canny(dst2, 50, 150)
    dst2 = cv2.GaussianBlur(dst2, (5, 5), 0)

    # for testing, show image after thresholding
    # cv2.imwrite('./out/%s-tempdst2.%s' % (0, 'jpg'), dst2)

    # find lines
    minLineLength = 10
    maxLineGap = 0
    lines = cv2.HoughLinesP(
        image=dst2,
        rho=3,
        theta=np.pi / 180,
        threshold=100,
        minLineLength=minLineLength,
        maxLineGap=0
    )  # rho is set to 3 to detect more lines, easier to get more then filter them out later

    # for testing purposes, show all found lines
    # for i in range(0, len(lines)):
    #     for x1, y1, x2, y2 in lines[i]:
    #         cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    #         cv2.imwrite('./out/%s-lines-test.%s' % (0, 'jpg'), img)

    # remove all lines outside a given radius
    final_line_list = []

    diff1LowerBound = 0  # diff1LowerBound and diff1UpperBound determine how close the line should be from the center
    diff1UpperBound = 0.5
    diff2LowerBound = 0  # diff2LowerBound and diff2UpperBound determine how close the other point of the line should be to the outside of the dashboard
    diff2UpperBound = 2

    for i in range(0, len(lines)):
        for x1, y1, x2, y2 in lines[i]:
            # x, y is center of circle
            diff1 = dist_2_pts(x, y, x1, y1)
            diff2 = dist_2_pts(x, y, x2, y2)
            # set diff1 to be the smaller (closest to the center) of the two, makes the math easier
            if (diff1 > diff2):
                temp = diff1
                diff1 = diff2
                diff2 = temp
            # check if line is within an acceptable range
            if (((diff1 < diff1UpperBound * r) and
                 (diff1 > diff1LowerBound * r) and
                 (diff2 < diff2UpperBound * r))
                    and (diff2 > diff2LowerBound * r)):
                line_length = dist_2_pts(x1, y1, x2, y2)
                # add to final list
                final_line_list.append([x1, y1, x2, y2])

    # testing only, show all lines after filtering
    max_length = 0
    xx1, yy1, xx2, yy2 = 0, 0, 0, 0
    for final_line in final_line_list:
        x1 = final_line[0]
        y1 = final_line[1]
        x2 = final_line[2]
        y2 = final_line[3]
        if dist_2_pts(x1, y1, x2, y2) > max_length:
            xx1, yy1, xx2, yy2 = x1, y1, x2, y2
            max_length = dist_2_pts(x1, y1, x2, y2)
        # cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # assumes the longest line is the best one
    x1, y1, x2, y2 = xx1, yy1, xx2, yy2
    # cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
    # cv2.imwrite('./out/%s-lines-filter.%s' % (0, 'jpg'), img)

    # find the farthest point from the center to be what is used to determine the angle
    dist_pt_0 = dist_2_pts(x, y, x1, y1)
    dist_pt_1 = dist_2_pts(x, y, x2, y2)
    if (dist_pt_0 > dist_pt_1):
        x_begin, x_end = x1, x2
        y_begin, y_end = y1, y2
    else:
        x_begin, x_end = x2, x1
        y_begin, y_end = y2, y1

    x_angle = x_begin - x_end
    y_angle = y_end - y_begin

    # take the arc tan of y/x to find the angle
    res = np.arctan(np.divide(float(y_angle), float(x_angle)))

    # these were determined by trial and error
    res = np.rad2deg(res)
    if x_angle > 0 and y_angle > 0:  # in quadrant I
        final_angle = 270 - res
    elif x_angle < 0 and y_angle > 0:  # in quadrant II
        final_angle = 90 - res
    elif x_angle < 0 and y_angle < 0:  # in quadrant III
        final_angle = 90 - res
    elif x_angle > 0 and y_angle < 0:  # in quadrant IV
        final_angle = 270 - res
    else:
        raise UserWarning('Pointer was not detected.')

    old_min = float(min_angle)
    old_max = float(max_angle)
    new_min = float(min_value)
    new_max = float(max_value)

    old_value = final_angle
    old_range = (old_max - old_min)
    new_range = (new_max - new_min)
    new_value = (((old_value - old_min) * new_range) / old_range) + new_min

    return new_value


if __name__ == '__main__':
    pass
