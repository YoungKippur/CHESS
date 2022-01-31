import cv2 as cv
import numpy as np
import time

point = (0,0)

circles = []
rectangles = []

aux = 0

board = ["a1","a2","a3","a4","a5","a6","a7","a8","b1","b2","b3","b4","b5","b6","b7","b8"]
BOARD = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

ESTADO = 0
AREA = 600

move1 = False
move2 = False

azulBajo = np.array([90, 100, 20], np.uint8)
azulAlto = np.array([120, 255, 255], np.uint8)

capture = cv.VideoCapture(1, cv.CAP_DSHOW)

def rescaleFrame(frame, scale=0.75):  # Rescalar el video (Default = 0.75) 
    width = int(frame.shape[1]  * scale)
    height = int(frame.shape[0] * scale)

    dimensions = (width,height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

def click(event, x,y, flags, param):
    global point, aux, ESTADO
    if event == cv.EVENT_LBUTTONDOWN and ESTADO == 0:
        point = (x,y)
        circles.append(point)
        aux = aux + 1
        if aux % 2 == 0:
            rectangles.append((circles[aux-1], circles[aux-2]))

cv.namedWindow("Frame")
cv.setMouseCallback("Frame", click)

while True:
    isTrue, frame1 = capture.read(0)
    frame1 = rescaleFrame(frame1, 1)

    for center_points in circles:
        cv.circle(frame1, center_points, 5, (0,0,255), -1)

    for center_points in rectangles:
        cv.rectangle(frame1, center_points[0], center_points[1], (0,255,255), 3)
        def1 = center_points[0][0] - center_points[1][0]
        def2 = center_points[0][1] - center_points[1][1]
        cent1 = int(center_points[0][0] - (def1 / 2))
        cent2 = int(center_points[0][1] - (def2 / 2))
        cv.putText(frame1, board[rectangles.index(center_points)], (cent1, cent2), cv.FONT_HERSHEY_SIMPLEX, .5, (0,255,0), 1, cv.LINE_AA)

    if ESTADO == 1:
        frameHSV = cv.cvtColor(frame1, cv.COLOR_BGR2HSV)
        mask = cv.inRange(frameHSV, azulBajo, azulAlto)
        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cv.drawContours(frame1, contours, -1, (0,255,0), 4)

        for c in contours:
            area = cv.contourArea(c)
            if area > AREA:
                M = cv.moments(c)
                if M['m00'] == 0:
                    M['m00'] = 1
                x = int(M['m10'] / M['m00'])
                y = int(M['m01'] / M['m00'])
                cv.circle(frame1, (x, y), 5 , (0,0,255), thickness=-1)
                newContour = cv.convexHull(c)
                cv.drawContours(frame1, [newContour], 0, (0,255,0), 3)

                if cv.waitKey(19) & 0xFF==ord("m"):
                    print("m")
                    for elem in rectangles:
                        if (x > elem[0][0] and x < elem[1][0]) or (x < elem[0][0] and x > elem[1][0]):
                            if (y > elem[0][1] and y < elem[1][1]) or (y < elem[0][1] and y > elem[1][1]):
                                if BOARD[rectangles.index(elem)] != 1:
                                    BOARD[rectangles.index(elem)] = 1
                                    sec = board[rectangles.index(elem)]
                                    move1 = True
                        else:
                            if BOARD[rectangles.index(elem)] != 0:
                                BOARD[rectangles.index(elem)] = 0
                                fir = board[rectangles.index(elem)]
                                move2 = True
                    
                    if move1 == True and move2 == True:
                        print(fir+sec)
                        move1 = False
                        move2 = False
                           
    cv.imshow('Frame', frame1)

    if cv.waitKey(19) & 0xFF==ord("f"):  # Tecla "f" para romper el while
        break

    if cv.waitKey(19) & 0xFF==ord("s"):
        ESTADO = 1

capture.release()
cv.destroyAllWindows()