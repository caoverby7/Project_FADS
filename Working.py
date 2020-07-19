#Import packages
import cv2
import argparse
from imutils import *
#import numpy as np
#from datetime import *
import time

#Code for initialization
videoStream = VideoStream(src=0).start()
time.sleep(3.0)
firstFrame = None
width=500

#Code for execution
#This is the main outter loop: Contains the core program. Continues until Q is pressed, then proceeds with cleanup and exit
while True:
    frame = videoStream.read()
    frame = frame[1]
    # resizing the frame
    frame = imutils.resize(frame, width=width)
    # convert each frame to grayscale
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayscale = cv2.GaussianBlur(grayscale, (21, 21), 0)
    #Sets firstframe to grayscale if firstFrame is "None"; Should happen once on program initialization
    if firstFrame is None:
        firstFrame = grayscale
        continue
 
    frameDelta = cv2.absdiff(firstFrame, grayscale)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    # dilate threshold image to fill in the holes  
    thresh = cv2.dilate(thresh, None, iterations=2)
    # 

    







    break
#Code for Cleanup and Exit, executed when Q is pressed
videoStream.release()
cv2.destroyAllWindows()