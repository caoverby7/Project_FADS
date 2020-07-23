import cv2
import time
from datetime import datetime
import numpy as np
#import imutils
import sys

#This function trys to create a log file
def createLogFile():
    try:
        logFile = open("Test_Event_Log.txt", "w+")
        writeToLog(logFile, "Event Log Initialized...")
        return logFile
    except:
        print("Log File failed to generate. Terminating program...")
        sys.exit()

#This function is called when an event is needed to be written to a log
def writeToLog(logFile, strEvent):
    logFile.write("["+getTimeStamp()+"] - "+strEvent+"\n")

#This function acquires a timestamp
def getTimeStamp():
    now = datetime.now()
    now = now.strftime("%d/%m/%Y %H:%M:%S")
    return now

#This function trys to initialized the camera feed
def startCapture(logFile):
    try:
        capture = cv2.VideoCapture(0)
        writeToLog(logFile, "Camera feed sucessfully acquired!")
        return capture
    except:
        writeToLog(logFile, "No camera detected. Closing Program...")
        logFile.close()
        sys.exit()

#This function displays the Video
def displayVideo(videoFrame):
    #Add timestamp to the video then display
    frame = cv2.putText(videoFrame, getTimeStamp(), (5,400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
    cv2.imshow("Fall Alert Detection System", videoFrame)

#This function closes the program
def closeProgram(logFile, capture):
    writeToLog(logFile, "Terminating Program...")
    logFile.close()
    capture.release()
    cv2.destroyAllWindows()
    sys.exit()

#This is the main function of the program
def main():
    firstFrame = None
    logFile = createLogFile()
    capture = startCapture(logFile)
    while True:
        #Read and modify frames
        ret, frame = capture.read()
        #Display Video
        displayVideo(frame)
        #Hotkey to break the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            closeProgram(logFile, capture)

#Script
if __name__ == "__main__":
    main()