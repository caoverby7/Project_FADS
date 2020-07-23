import cv2
import time
from datetime import datetime
import numpy as np
#import imutils
import sys

#This function acquires a timestamp
def getTimeStamp():
    now = datetime.now()
    now = now.strftime("%d/%m/%Y %H:%M:%S")
    return now

#This function closes the program
def closeProgram():
    writeToLog(logFile, "Terminating Program...")
    logFile.close()
    cap.release()
    cv2.destroyAllWindows()
    sys.exit()

#This function trys to create a log file
def createLogFile():
    try:
        logFile = open("Test_Event_Log.txt", "w+")
        writeToLog(logFile, "Event Log Initialized...")
        return logFile
    except:
        print("Log File failed to generate. Terminating program...")
        sys.exit()

#This function trys to initialized the camera feed
def startCapture(logFile):
    try:
        cap = cv2.VideoCapture(0)
        writeToLog(logFile, "Camera feed sucessfully acquired!")
        return cap
    except:
        writeToLog(logFile, "No camera detected. Closing Program...")
        logFile.close()
        sys.exit()

#This function displays the Video
def displayVideo(videoFrame):
    #Add timestamp to the video then display
    frame = cv2.putText(videoFrame, getTimeStamp(), (5,400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
    cv2.imshow("Fall Alert Detection System", videoFrame)

#This function is called when an event is needed to be written to a log
def writeToLog(logFile, strEvent):
    logFile.write("["+getTimeStamp()+"] - "+strEvent+"\n")

#This is the main function of the program
def main():
    firstFrame = None
    logFile = createLogFile()
    cap = startCapture(logFile)
    while True:
        #Read and modify frames
        ret, frame = cap.read()
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gaussFrame = cv2.GaussianBlur(grayFrame, (9,9), 0)
        #Get the first frame
        if firstFrame is None:
            firstFrame = gaussFrame
            writeToLog(logFile, "First Frame Fetched")

            continue
        deltaFrame = cv2.absdiff(firstFrame, gaussFrame)
        threshFrame = cv2.threshold(deltaFrame, 25, 255, cv2.THRESH_BINARY)
        #Display Video
        displayVideo(frame)
        #Hotkey to break the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            closeProgram()

#Script
if __name__ == "__main__":
    main()