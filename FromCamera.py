
import numpy as np
import matplotlib.image as mpimg
import cv2
from docopt import docopt
from IPython.display import HTML, Video
from moviepy.editor import VideoFileClip
from CameraCalibration import CameraCalibration
from Thresholding import *
from PerspectiveTransformation import *
from LaneLines import *

class FindLaneLines:
    """ This class is for parameter tunning.

    Attributes:
        ...
    """
    def __init__(self):
        """ Init Application"""
        # Kamera Kalibrasi : untuk mengurangi error yang ditangkap kamera
        
        self.calibration = CameraCalibration('camera_cal', 9, 6)
        self.thresholding = Thresholding()
        self.transform = PerspectiveTransformation()
        self.lanelines = LaneLines()

    def forward(self, img):
        out_img = np.copy(img)
        img = self.calibration.undistort(img)
        img = self.transform.forward(img)
        img = self.thresholding.forward(img)
        img = self.lanelines.forward(img)
        img = self.transform.backward(img)

        out_img = cv2.addWeighted(out_img, 1, img, 0.6, 0)
        out_img = self.lanelines.plot(out_img)
        return out_img

#     def process_image(self, input_path, output_path):
#         img = mpimg.imread(input_path)
#         out_img = self.forward(img)
#         # print(out_img)
#         mpimg.imsave(output_path, out_img)

    def process_video(self, input):
        clip = input.fl_image(self.forward)

#     def process_video(self, input_path, output_path):
#         clip = VideoFileClip(input_path)
#         out_clip = clip.fl_image(self.forward)
#         out_clip.write_videofile(output_path, audio=False)

def main():
    findLaneLines = FindLaneLines()
    
    cap = cv2.VideoCapture('test_videos/11_test.mp4')

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        _, img = cap.read()

        out_img = np.copy(img)

        result = findLaneLines.forward(out_img)

        cv2.imshow("Lane Assist", result)

        k = cv2.waitKey(30)
        if k%256 == 27:
        # ESC pressed
            print("Escape hit, closing...")
            break
          
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()