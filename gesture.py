import math
import cv2 as cv
import numpy as np


#def nothing(x):
#    pass

def gesture_use():
    # Get camera feed. May need to experiment with integers to get the correct one.
    cap = cv.VideoCapture(0)

    #used to determine ranges of mask
    #cv.namedWindow("mask")
    #cv.createTrackbar("lower","mask",0,255,nothing)
    #cv.createTrackbar("upper","mask",0,255,nothing)

    while True:
        # Read each frame on the camera.
        _, frame = cap.read()

        # create a yellow square(canvas) on the frame.
        pt1 = 0    # The origin
        pt2 = 250   # the Length and Width
        yellow = (0, 234, 255)  # Note: Color is BGR
        cv.rectangle(frame, (pt1, pt1), (pt2,pt2), yellow, 5)
        canvas = frame[pt1:pt2, pt1:pt2]

        # convert the canvas to grayscale
        gray = cv.cvtColor(canvas, cv.COLOR_BGR2GRAY)

        # Apply median blur to the canvas to smooth the image and remove noise.
        smooth = cv.medianBlur(gray, 3)
        #cv.imshow("canvas", smooth)

        # Find the hand in the canvas
        lower = 1
        upper = 135
        #lower = cv.getTrackbarPos("lower","mask")
        #upper = cv.getTrackbarPos("upper","mask")
        binary = cv.inRange(smooth, lower, upper)
        cv.imshow("mask", binary)


        # find contours. 
        # contours is a python list of all the contours in the image. Each individual contour is a np array of (x,y) coordinates of boundary points of the object.
        contours, hierarchy = cv.findContours(binary, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
        
        # checks if any elements in contours list, otherwise error if none.
        if len(contours) > 0:
            # get the biggest contour, to exclude some noise. Assuming biggest contour is the hand.
            big_contour = max(contours, key=cv.contourArea) 
            # draw contours
            index = -1  # -1 is for all of them.
            red = (0, 0, 255)
            thickness = 3
            cv.drawContours(frame, big_contour, index, red, thickness)

            # Convex Hull algorithm and draw the contours
            blue = (255, 0, 0)
            c_hull = [cv.convexHull(big_contour)]
            cv.drawContours(frame, c_hull, index, blue, thickness)
            
            # find the convexity defects
            c_hull = cv.convexHull(big_contour, returnPoints=False)
            defects = cv.convexityDefects(big_contour, c_hull)
            #print("start")
            #print(defects)


        # Render frame to the screen .
        cv.imshow("Camera", frame)

        # if 'q' is pressed, then end the loop.
        if cv.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv.destroyAllWindows()


#import cv2 as cv
#import mediapipe as mp
#
#
#def gesture_use():
#    # Getting camera feed. May need to experiment with integers to get the correct one.
#    cap = cv.VideoCapture(0)
#
#    # Variables to utilize mp solutions drawing_utils.py and hands.py
#    mp_drawing = mp.solutions.drawing_utils
#    mp_hands = mp.solutions.hands
#
#    # by default there are 2 hands but only need to track 1
#    hand = mp_hands.Hands(max_num_hands=1)
#
#    while True:
#        # Read each frame on the camera.
#        ret, frame = cap.read()
#
#        # Processes an RGB image and returns the hand landmarks and handedness detected for a hand.
#        detections = hand.process(frame)
#
#        # For devs to see if a hand is being tracked. Can be commented out later.
#        if detections.multi_hand_landmarks:
#            for marker in detections.multi_hand_landmarks:
#                # Draw the landmarks onto the tracked hand.
#                mp_drawing.draw_landmarks(frame, marker, mp_hands.HAND_CONNECTIONS)
#
#        # list the landmarks on the current frame
#        landmark_list = []
#        if detections.multi_hand_landmarks:
#            for marker in detections.multi_hand_landmarks:
#                for element, lm in enumerate(marker.landmark):
#                    landmark_list.append([lm.x, lm.y])
#
#        # Boolean list of which finger is extended. index=0, middle=1, ring=2, pinky=3
#        finger_list = []
#        if len(landmark_list) == 21:
#            x = 0
#            y = 1
#            # for the Index finger
#            finger_list.append(landmark_list[8][y] < landmark_list[7][y])
#            # for middle finger
#            finger_list.append(landmark_list[12][y] < landmark_list[11][y])
#            # for ring finger
#            finger_list.append(landmark_list[16][y] < landmark_list[15][y])
#            # for pinky finger
#            finger_list.append(landmark_list[20][y] < landmark_list[19][y])
#        # print the list
#        if len(finger_list) != 0:
#            print(finger_list, sep=", ", end="\n")
#
#        # Render frame to the screen .
#        cv.imshow("Camera", frame)
#
#        # when 'q' is pressed, then end the loop.
#        if cv.waitKey(1) & 0xFF == ord("q"):
#            break
#
#    cap.release()
#    cv.destroyAllWindows()