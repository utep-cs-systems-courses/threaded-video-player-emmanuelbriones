#!/usr/bin/env python3

import cv2
import threading
from queue import queue 

VIDEOFILE = "../clip.mp4" # path to the video
DELIMITER = "\0"
FRAMEDELAY = 42

def extractFrames(fileName, frameQueue):
    # check if null
    if fileName is None:
        raise TypeError
    if frameQueue is None:
        raise TypeError

    count = 0 # frame count

    vidcap = cv2.VideoCapture(fileName)

    # reads one frame
    success, image = vidcap.read()

    print(f'Reading frame {count} {success}')
    while success:
        # add frame to queue
        frameQueue.put(image)

        success, image = vidcap.read()
        print(f'Reading frame {count} {success}')
        count += 1

    print('Finished extracting frames'); # end 
    frameQueue.put(DELIMITER)
