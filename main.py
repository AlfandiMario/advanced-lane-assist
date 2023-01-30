"""
Lane Lines Detection pipeline

Usage:
    main.py [--video] OUTPUT_PATH INPUT_PATH

Options:

-h --help                               show this screen
--video                                 process video file instead of image
"""

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

    def process_image(self, input_path, output_path):
        img = mpimg.imread(input_path)
        out_img = self.forward(img)
        # print(out_img)
        mpimg.imsave(output_path, out_img)

    # def process_video(self, input):
    #     clip = input
    #     out_clip = clip.fl_image(self.forward)
        # out_clip.write_videofile(output_path, audio=False)

    def process_video(self, input_path, output_path):
        clip = VideoFileClip(input_path)
        out_clip = clip.fl_image(self.forward)
        out_clip.write_videofile(output_path, audio=False)

def main():
    args = docopt(__doc__)

    output = args['OUTPUT_PATH']
    # output = 'output_videos/hasil.png'
    input = args['INPUT_PATH']
    # input = 'left_turn.png'

    findLaneLines = FindLaneLines()

    if args['--video']:
        findLaneLines.process_video(input, output)
    else:
        findLaneLines.process_image(input, output)

    # cap = cv2.VideoCapture(0)

    # while True:
    #     if not cap.isOpened():
    #         print("Cannot open camera")
    #         exit()
    #     ret, input = cap.read()
    

    #     findLaneLines = FindLaneLines()
    #     result = findLaneLines.process_video(input)
    #     cv2.imshow("Lane Assist", result)

    #     k = cv2.waitKey(100)
    #     if k%256 == 27:
    #       # ESC pressed
    #       print("Escape hit, closing...")
    #       break

    # cap.release()
    # cv2.destroyAllWindows()


if __name__ == "__main__":
    main()