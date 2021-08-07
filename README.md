# DrawsyDetector
#### This is a program that was written using python. I used the following libraries to implement this program.
    - 💠 openCV
    - 🧊 numpy
    - ⚙️ dlib
    - 🔉 vlc
    
## The goal of the project
#### The goal of this project was to create a prototype of a program that can be built on so that It can help in avoiding drowsy driving and potentially save lives by preventing car accients during long drives.


## How it works?
#### The above modules used in this program explain how this program was implemented. 
- OpenCV is used to access real time video feed form the device that the program is running on 
- numpy is used to handle the array based calculations such as the Eucleadian distance to calculate the distance between two points. 
- The points in our case are landmarks of differnt points on our face that the dlib module provides.
- vlc module is used to play the alerts that awake users after the users state has been determined

## The facial landmarks that dlib provides are shown below
<img src =https://github.com/Nlege001/DrawsyDetector/blob/master/facial_landmarks_68markup.jpg width = 500>

## Explanation of the taught process
#### So as you can see, if we calculate the distance between these landmarks and compare them to an accpted distance, we can actually determine if a user is drowsy or not (i.e if the users pupil size is smaller than expected or smaller than their active state, this program determines if they are drowsy or not). However the results can vary depending on what type of camera is used (quality) and also from person to person.

### This is what the following code snippet is trying to do
```python
# The function below calculates the Euclidean distance between two points and returns that distance
def compute(point_A, point_B):
    dist = np.linalg.norm(point_A - point_B)
    return dist
```

### Then the following function uses the above function so that it can calculate specific distances between selected landmarks on the face
```python
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
```

### Then we detect the face of the user and we set the landmakrs on the video input and do our calculations to determine whether the users is drowsy or not.
### We have three possible outcomes:
- Active (user is fully awake)
- Sleepy (an alert is played by the vlc module so that the user awakes)
- Drowsy (an alert is played to make the user active)
    
    
### Feel free to clone and see how this program works. Enjoy!

    
    

      
