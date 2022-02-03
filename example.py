"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from gaze_tracking import GazeTracking

import autopy
from matplotlib import pyplot as plt
import seaborn as sns

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
screen_resolution = autopy.screen.size()

if webcam.isOpened():
    video_resolution = (
        webcam.get(cv2.CAP_PROP_FRAME_WIDTH),
        webcam.get(cv2.CAP_PROP_FRAME_HEIGHT),
    )
else:
    video_resolution = None

screen_x=1366
screen_y=768
def transform_video_coordinates_to_screen(eye_x_pos, eye_y_pos):
    if not video_resolution:
        return (eye_x_pos, eye_y_pos)

    return (
        eye_x_pos / video_resolution[0] * screen_resolution[0],
        eye_y_pos / video_resolution[1] * screen_resolution[1],
    )

x=600
y=600
while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        text = "Blinking"
    elif gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"
    if  gaze.is_blinking():
        pass
    else:
        x_ratio = gaze.horizontal_ratio()

        y_ratio = gaze.vertical_ratio()
        print(y_ratio)
        try:
            if y_ratio>=(0.51):
                y+=5
            elif y_ratio<=(0.49):
                y-=5
            else:
                y=384
            # if gaze.is_center():
            #     y = 384
        except:
            pass

        if gaze.is_right():
            x+=5
        elif gaze.is_left():
            x-=5
        autopy.mouse.move(x, y)

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:
        break
   
webcam.release()
cv2.destroyAllWindows()
