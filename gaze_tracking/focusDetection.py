import cv2
import sys

sys.path.insert(2, 'GazeTracking')
from .gaze_tracking import GazeTracking

#example:
my_img = cv2.imread('F:/project_image/GazeTracking/images.jpg')

class focusDetector:
    def __init__(self):
        self.gaze = GazeTracking()

    def focused(self, frame):
        self.gaze.refresh(frame)
        frame = self.gaze.annotated_frame()
        res = "focused"
        if self.gaze.is_blinking():
            res = "blink"
        elif self.gaze.is_right():
            res = "right"
        elif self.gaze.is_left():
            res = "left"
        elif self.gaze.pupil_right_coords()==None or self.gaze.pupil_left_coords()==None:
            res = "Not focused"
        return res


# if __name__ == '__main__':
#     res = focused(my_img)
#     print(res)