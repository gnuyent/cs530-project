import cv2 as cv

# Does nothing, required to use opencv2's createTrackbar.
def nothing(x):
    pass


def gesture_use():
    # Get camera feed. May need to experiment with integers to get the correct one.
    cap = cv.VideoCapture(0)

    # Used to determine ranges of binary images Threshold
    # lower and upper values are set to a specific threshold.
    # Can meet the users needs if the initial threshold
    # isnt selecting the correct object for the user. The
    # trackbar has two boundaries, lower and upper bounds.
    lower_val = 0
    upper_val = 135
    cv.namedWindow("Binary Threshold")
    cv.createTrackbar("lower", "Binary Threshold", lower_val, 255, nothing)
    cv.createTrackbar("upper", "Binary Threshold", upper_val, 255, nothing)

    # colors used in the program. Important Note: Colors are BGR and not RGB
    yellow = (0, 234, 255)
    red = (0, 0, 255)
    green = (0, 255, 0)
    white = (255, 255, 255)

    while True:
        # Read each frame on the camera.
        _, frame = cap.read()

        # create a yellow square(canvas) on the frame.
        pt1 = 0  # The origin
        pt2 = 250  # the Length and Width
        cv.rectangle(frame, (pt1, pt1), (pt2, pt2), yellow, 5)
        canvas = frame[pt1:pt2, pt1:pt2]

        # convert the canvas to grayscale
        gray = cv.cvtColor(canvas, cv.COLOR_BGR2GRAY)

        # Apply Median Blurring to the canvas to smooth the image and remove noise.
        smooth = cv.medianBlur(gray, 3)

        # Finds the hand in the canvas based on the threshold values. Displays a
        # black and white image for the user. Trackbar can be manipulated to obtain
        # the correct threshold. Note: White Pixel means the object is being detected.
        lower = cv.getTrackbarPos("lower", "Binary Threshold")
        upper = cv.getTrackbarPos("upper", "Binary Threshold")
        binary = cv.inRange(smooth, lower, upper)
        cv.imshow("Binary Threshold", binary)

        # find contours.
        # contours is a python list of all the contours in the image. Each individual
        # contour is a np array of (x,y) coordinates of boundary points of the object.
        contours, hierarchy = cv.findContours(
            binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE
        )

        # checks if there is any set of contours in the list. Mainly used to prevent error if none.
        if len(contours) > 0:
            # get the biggest contour, to exclude some noise. Assuming biggest contour is the hand.
            big_contour = max(contours, key=cv.contourArea)

            # draw contours
            index = -1  # -1 is for all of them.
            thickness = 3  # the thickness of the contours.
            cv.drawContours(frame, big_contour, index, red, thickness)

            # returnpoints = false, returns index instead of the actual points
            # convex hull is used to find the defects in the contour line.
            c_hull = cv.convexHull(big_contour, returnPoints=False)
            defects = cv.convexityDefects(big_contour, c_hull)

            # Count the defects. Count incremented when it's greater than a certain distance.
            count = 0

            # The if-statement prevents crashing when defects is none.
            if type(defects) != type(None):
                for i in range(defects.shape[0]):
                    s, e, f, d = defects[i, 0]

                    # If-statement acts like a theshold for the set of defects.
                    # d is the approximate distance from the farthest point.
                    if d > 3000:
                        start = tuple(big_contour[s][0])
                        end = tuple(big_contour[e][0])
                        far = tuple(big_contour[f][0])

                        # for devs to see a green line between fingers
                        cv.line(frame, start, end, green, 2)

                        # for devs to see where the defects are. 
                        cv.circle(frame, far, 5, white, -1)
                        
                        # Increment count when d is above the threshold.
                        count = count + 1

            # TODO all this does is display the current count of the fingers in the terminal.
            print(count)

        # Render frame to the screen.
        cv.imshow("Camera", frame)

        # if 'q' is pressed, then end the loop.
        if cv.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv.destroyAllWindows()


# import cv2 as cv
# import mediapipe as mp
#
#
# def gesture_use():
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
