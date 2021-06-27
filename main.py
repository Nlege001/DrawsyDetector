######################## This is a program that detects drawsiness form facial features ######################

# This project was a self tought project and source include python and Dlib documentation, online courses and
# Mastering openCV4 with python book by PacktHub


# importing Modules
import cv2
import numpy as np
import dlib
from imutils import face_utils
import vlc

# This opens the webcam and takes an instance of it. Usually the index to pass is 1
# but in our case we use one as the id associated with the webcam is 1.
cap = cv2.VideoCapture(1)

# This opens the default face detector and also the 68 landmarks of face detection which
# are located in the same file as this program
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# states
sleepy = 0
drowsy = 0
active = 0
status = ""
color = (0, 0, 0)

# The function below calculates the Euclidean distance between two points and returns that distance
def compute(point_A, point_B):
    dist = np.linalg.norm(point_A - point_B)
    return dist

# The function below will use the above Euclidean distance calculating function to roughly estimate whether
# the user has is_blinking by detecting the distance between the eye landmarks (37,38,39,40,41,42- left eye and
# 43,44,45,46,47,48- - right eye)

# Depending on the eye size and webcam quality, results might vary

def is_blinking(a, b, c, d, e, f):
    up = compute(b, d) + compute(c, e)
    down = compute(a, f)
    ratio = up / (2.0 * down)

    
    if (ratio > 0.25):
        return 2
    elif (ratio > 0.21 and ratio <= 0.25):
        return 1
    else:
        return 0

# This is an infinte loop that will be broken later by a break statment.
while True:
    ret, frame = cap.read()                               # This line defines a return and a frame as cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)        # we define an new variable gray as the frame

    faces = detector(gray)  # we run the default face detector we imported on gray(our frame) and assign the value to a new vairable faces

# The loop below will locate the face and will create a green frame around it indicating succesful detection
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        face_frame = frame.copy()  # we are creating a copy of our orginal frame so that we can locate the landmarks(68 in number) inside the lcoated face
        cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2) # this is the actual line where we draw the rectangle(green in color. i.e (0,255,0)) on the detected face

        landmarks = predictor(gray, face) # this uses the face detection file we imported to predict the landmarks of the features of the users face
        landmarks = face_utils.shape_to_np(landmarks) # this converts the prediction of our landmarks to a numpy array

        #The variables below are defualt landmarks of the left and right eye
        left_blink = is_blinking(landmarks[36], landmarks[37],
                             landmarks[38], landmarks[41], landmarks[40], landmarks[39])
        right_blink = is_blinking(landmarks[42], landmarks[43],
                              landmarks[44], landmarks[47], landmarks[46], landmarks[45])

        # The if statement below runs the is_blinking function to determine if eyes are closed or open and states are updated
        if (left_blink == 0 or right_blink == 0):
            sleepy += 1
            drowsy = 0
            active = 0
            sound_file = vlc.MediaPlayer("/Users/naol/PycharmProjects/DrawsyDetector/alertSound.mp3")
            if (sleepy > 6):
                status = "SLEEPING...ALERT !!!"
                color = (255, 0, 0)  # BLUE COLOR
                sound_file.play()


        elif (left_blink == 1 or right_blink == 1):
            sleepy = 0
            active = 0
            drowsy += 1
            if (drowsy > 6):
                status = "DROWSY....ALERT !"
                color = (0, 0, 255)  # RED COLOR

        else:
            drowsy = 0
            sleepy = 0
            active += 1
            if (active > 6):
                status = "ACTIVE"
                color = (0, 255, 0)  # GREEN COLOR

        cv2.putText(frame, status, (500, 500), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)   # print the state on the frame

        # The loop below displays all 68 landmarks on the orginal frame as white dots
        for n in range(0, 68):
            (x, y) = landmarks[n]
            cv2.circle(face_frame, (x, y), 1, (255, 255, 255), -1)

    # we have two frames, one that shows the facial detection and the other that shows the state of the user
    cv2.imshow("Face detection Frame", frame)
    cv2.imshow("State detection Frame", face_frame)
    key = cv2.waitKey(5)
    if key == 'q':   # quit is q is pressed
        break
