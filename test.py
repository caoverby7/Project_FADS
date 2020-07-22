import cv2
import time
from datetime import datetime
import numpy as np
#import imutils
import sys

#This function acquires a timestamp for logging
def getLogTimeStamp():
    now = datetime.now()
    now = now.strftime("%d/%m/%Y %H:%M:%S")
    return now

#This function acquires a timestamp for the video feed
def getFeedTimeStamp():
    now = datetime.now()
    now = now.strftime("%d/%m/%Y %H:%M:%S")
    return now

#This function closes the program
def closeProgram():
    logFile.write(getLogTimeStamp()+" --- Terminating Program...\n")
    logFile.close()
    cap.release()
    cv2.destroyAllWindows()

#This function trys to create a log file
def createLogFile():
    try:
        logFile = open("Test_Event_Log.txt", "w+")
        logFile.write(getLogTimeStamp()+" --- Event Log Initialized...\n")
        return logFile
    except:
        print("Log File failed to generate. Terminating program...")
        sys.exit()

#This function trys to initialized the camera feed
def startCapture():
    try:
        cap = cv2.VideoCapture(0)
        logFile.write(getLogTimeStamp()+" --- Camera feed sucessfully acquired!\n")
        return cap
    except:
        print("Log File failed to generate. Terminating program...")
        logFile.write(getLogTimeStamp()+" --- No camera detected. Closing Program...\n")
        logFile.close()
        sys.exit()



firstFrame = None
font = cv2.FONT_HERSHEY_SIMPLEX
logFile = createLogFile()
cap = startCapture()
while True:
    #Read and modify frames
    ret, frame = cap.read()
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gaussFrame = cv2.GaussianBlur(grayFrame, (9,9), 0)
    #Get the first frame
    if firstFrame is None:
        firstFrame = gaussFrame
        logFile.write(getLogTimeStamp()+" --- "+"First Frame Fetched\n")
        continue
    deltaFrame = cv2.absdiff(firstFrame, gaussFrame)
    threshFrame = cv2.threshold(deltaFrame, 25, 255, cv2.THRESH_BINARY)
    #Place timestamp on frame
    frame = cv2.putText(frame, getFeedTimeStamp(), (5,400), font, 1, (0, 0, 255), 1)
    #Display frames in specific windows
    cv2.imshow("gray feed",grayFrame)
    cv2.imshow("Gaussian feed", gaussFrame)
    cv2.imshow("test feed", frame)
    cv2.imshow("delta", deltaFrame)
    #cv2.imshow("thresh", threshFrame)

    #Hotkey to break the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

closeProgram()