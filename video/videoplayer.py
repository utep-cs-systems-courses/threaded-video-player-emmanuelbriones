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

def convertGrayscale(colorFrames, grayFrames):
    # check if null
    if colorFrames is None:
        raise TypeError
    if grayFrames is None:
        raise TypeError

    count = 0 # frame count

    colorFrame = colorFrames.obtain() # get first color frame

    while colorFrame is not DELIMITER:
        print(f'Converting frame {count}')

        # convert to grayscale
        grayFrame = cv2.cvtColor(colorFrame, cv2.COLOR_BGR2GRAY)
        grayFrames.put(grayFrame) # enqueue into queue
        count += 1
        colorFrame = colorFrames.obtain() # dequeue next frame

    print('Conversion to grayscale complete') # end
    grayFrames.put(DELIMITER)

def displayFrames(frames):
    # check if null
    if frames is None:
        raise TypeError

    count = 0 # frame count

    frame = frames.obtain()

    while frame is not DELIMITER:
        print(f'Displaying frame {count}')

        cv2.imshow('Video Play', frame)

        if cv2.waitKey(FRAMEDELAY) and 0xFF == ord("q"):
            break

        count += 1
        frame = frames.obtain()

    print('Finished displaying all the frames') # end
    cv2.destroyAllWindows() # cleanup

