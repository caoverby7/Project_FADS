import cv2
import time
from datetime import datetime
import numpy as np
#import imutils
import sys
import argparse


#This function inizilizes the program
def initializeProgram():
    try:
        createLogFile()
        capture = startCapture()
        writeToLog("Program fully initilized!")
        bgReduct = cv2.createBackgroundSubtractorMOG2()
        frameWidth = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        frameHeight = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(frameWidth, frameHeight)
        return capture, bgReduct, frameWidth, frameHeight
    except:
        writeToLog(logFile, "ERROR: Initilization failed!")
        sys.exit()

#This function trys to create a log file
def createLogFile():
    try:
        logFile = open("Test_Event_Log.txt", "a+")
        logFile.write("********************New Initialization********************\n\n")
        logFile.close()
        writeToLog("Event Log Initialized!")
    except:
        print("Log File failed to generate. Terminating program...")
        sys.exit()

#This function is called when an event is needed to be written to a log
def writeToLog(strEvent):
    logFile = open("Test_Event_Log.txt", "a+")
    logFile.write("["+getTimeStamp()+"] - "+strEvent+"\n")
    logFile.close()

#This function acquires a timestamp
def getTimeStamp():
    now = datetime.now()
    now = now.strftime("%d%b%Y %H%M%S")
    return now

#This function trys to initialized the camera feed
def startCapture():
    try:
        #capture = cv2.VideoCapture(0)
        capture = cv2.VideoCapture('TEST_Walking.mp4')
        writeToLog("Camera feed sucessfully acquired!")
        return capture
    except:
        writeToLog("No camera detected. Closing Program...")
        sys.exit()

#This function modifies the video frames
def modifyFrames(frame, bgReduct):
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fgmask = bgReduct.apply(grayscale)
    return fgmask

#This function implements motion tracking

#This function displays the Video
def displayVideo(videoFrame):
    #Add timestamp to the video then display
    #frame = cv2.putText(videoFrame, getTimeStamp(), (5,400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
    cv2.imshow("Fall Alert Detection System", videoFrame)

#This function closes the program
def closeProgram(capture):
    writeToLog("Terminating Program...\n\n\n\n")
    capture.release()
    cv2.destroyAllWindows()
    sys.exit()

#This is the main function of the program
def main():
    capture, bgReduct, frameWidth, frameHeight = initializeProgram()
    while (True):
        #Read and modify frames
        ret, frame = capture.read()
        #modify frames
        fgmask = modifyFrames(frame, bgReduct)
        # #Display Video
        displayVideo(fgmask)
        #Hotkey to break the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    closeProgram(capture)

#Script
if __name__ == "__main__":
    main()