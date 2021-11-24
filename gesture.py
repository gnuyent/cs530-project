import cv2 as cv
import mediapipe as mp


def gesture_use():
    # Getting camera feed. May need to experiment with integers to get the correct one.
    cap = cv.VideoCapture(0)

    # Variables to utilize mp solutions drawing_utils.py and hands.py
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    # by default there are 2 hands but only need to track 1
    hand = mp_hands.Hands(max_num_hands=1)

    while True:
        # Read each frame on the camera.
        ret, frame = cap.read()

        # Processes an RGB image and returns the hand landmarks and handedness detected for a hand.
        detections = hand.process(frame)

        # For devs to see if a hand is being tracked. Can be commented out later.
        if detections.multi_hand_landmarks:
            for marker in detections.multi_hand_landmarks:
                # Draw the landmarks onto the tracked hand.
                mp_drawing.draw_landmarks(frame, marker, mp_hands.HAND_CONNECTIONS)

        # list the landmarks on the current frame
        landmark_list = []
        if detections.multi_hand_landmarks:
            for marker in detections.multi_hand_landmarks:
                for element, lm in enumerate(marker.landmark):
                    landmark_list.append([lm.x, lm.y])

        # Boolean list of which finger is extended. index=0, middle=1, ring=2, pinky=3
        finger_list = []
        if len(landmark_list) == 21:
            x = 0
            y = 1
            # for the Index finger
            finger_list.append(landmark_list[8][y] < landmark_list[7][y])
            # for middle finger
            finger_list.append(landmark_list[12][y] < landmark_list[11][y])
            # for ring finger
            finger_list.append(landmark_list[16][y] < landmark_list[15][y])
            # for pinky finger
            finger_list.append(landmark_list[20][y] < landmark_list[19][y])
        # print the list
        if len(finger_list) != 0:
            print(finger_list, sep=", ", end="\n")

        # Render frame to the screen .
        cv.imshow("Camera", frame)

        # when 'q' is pressed, then end the loop.
        if cv.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv.destroyAllWindows()
