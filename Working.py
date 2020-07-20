#Import packages
from imutils.video import VideoStream
import argparse
import cv2
import argparse
import imutils
#import numpy as np
from datetime import *
import time

#Code for initialization; Logs to log file
ap = argparse.ArgumentParser()
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

logFile = open("FADS_Event_Log.txt", "w+")
now = datetime.now()
logFile.write(now.strftime("%d/%m/%Y %H:%M:%S")+" --- "+"Program Initialized...\n"+now.strftime("%d/%m/%Y %H:%M:%S")+" --- "+"Log File Initialized...\n")
videoStream = VideoStream(src=0).start()
time.sleep(3.0)
now = datetime.now()
logFile.write(now.strftime("%d/%m/%Y %H:%M:%S")+" --- "+"Camera Connected\n")
firstFrame = None
width=500


#Code for execution
#This is the main outter loop: Contains the core program. Continues until Q is pressed, then proceeds with cleanup and exit
while True:
    #Setting up frames
    frame = videoStream.read()
    frame = frame if args.get("video", None) is None else frame[1]
    # resizing the frame
    frame = imutils.resize(frame, width=width)
    # convert each frame to grayscale
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayscale = cv2.GaussianBlur(grayscale, (21, 21), 0)
    #Sets firstframe from frame if fire pass; Should only happen once. Logs event to log file
    if firstFrame is None:
        firstFrame = grayscale
        now = datetime.now()
        logFile.write(now.strftime("%d/%m/%Y %H:%M:%S")+" --- "+"First Frame Fetched\n")
        continue
    frameDelta = cv2.absdiff(firstFrame, grayscale)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    # dilate threshold image to fill in the holes  
    thresh = cv2.dilate(thresh, None, iterations=2)
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    #cntArea = cv2.contourArea(contours)
    # loop over the countours
    for c in contours:
        # ignore if contour is too small
        if cv2.contourArea(c) < args["min_area"]:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("Fall Alert Detection System", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        now = datetime.now()
        logFile.write(now.strftime("%d/%m/%Y %H:%M:%S")+" --- "+"Program exit initialized...\n")
        break
#Code for Cleanup and Exit, executed when Q is pressed
now = datetime.now()
logFile.write(now.strftime("%d/%m/%Y %H:%M:%S")+" --- "+"Closing Log File and exiting program.\n")
logFile.close()
videoStream.release()
cv2.destroyAllWindows()