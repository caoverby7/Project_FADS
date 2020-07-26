import cv2
import time
from datetime import datetime
import numpy as np
import imutils
from imutils.video import VideoStream
import sys
import argparse
import threading
import ctypes

#Globals
fallState = False
prevFallState = False
startTimer = 0
currentTimer = 0

#This function inizilizes the program
def initializeProgram():
    try:
        createLogFile()
        ap = argparse.ArgumentParser()
        ap.add_argument("-a", "--min-area", type=int, default=4000, help="minimum area size")
        args = vars(ap.parse_args())
        firstFrame= None
        capture = startCapture()
        writeToLog("Program fully initilized!")
        frameWidth = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        frameHeight = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return args, firstFrame, capture, frameWidth, frameHeight
    except:
        writeToLog("ERROR: Initilization failed!")
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
        capture = cv2.VideoCapture('test.mp4')
        writeToLog("Camera feed sucessfully acquired!")
        return capture
    except:
        writeToLog("No camera detected. Closing Program...")
        sys.exit()

#This function implements processes the video
def processVideo(frame, args, firstFrame):
    text = "No movement detected."
    frame = imutils.resize(frame, width=500)
    frameGray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    frameBlur = cv2.GaussianBlur(frameGray, (21, 21), 5)
    if firstFrame is None:
        firstFrame = frameBlur
    frameDelta = cv2.absdiff(firstFrame, frameBlur)
    frameThresh = cv2.threshold(frameDelta, 20, 255, cv2.THRESH_BINARY)[1]
    frameDilate = cv2.dilate(frameThresh, None, iterations=15)
    contoursFind = cv2.findContours(frameDilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contoursGrab = imutils.grab_contours(contoursFind)
    for c in contoursGrab:
        if cv2.contourArea(c) < args["min_area"]:
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = monitorSubject(w,h)
    return frame, firstFrame, text

#This function monitors a subject when in frame
def monitorSubject(xaxis, yaxis):
    x = int(xaxis)
    y = int(yaxis)
    prevFallState = fallState
    if x>y:
        fallState = True
        return "Fall"
    elif y<=x:
        fallState = False
        return "Safe"
    else:
        fallState = False
        return "No movement detected."

#This function sends an alert
#def sendAlert():
    #Code goes here

#This handles the timer start
def alertTimer():
    if (prevFallState == False && fallStae == True):
        startTimer = time.time()
    elif (prevFallState == True && fallState == True):
        currentTimer = time.time() - startTimer
        if currentTimer == 60:
            sendAlert()
    elif (prevFallState == True && fallState == False):
        startTimer = 0
    else:
     startTimer = 0
    

#This is the code for the alert box
def alertBox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

#This function displays the Video
def displayVideo(frame, text):
    #Add timestamp to the video then display
    frame = cv2.putText(frame, getTimeStamp(), (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow("Fall Alert Detection System", frame)

#This function closes the program
def closeProgram(capture):
    writeToLog("Terminating Program...\n\n\n")
    capture.release()
    cv2.destroyAllWindows()
    sys.exit()

#This is the main function of the program
def main():
    args, firstFrame, capture, frameWidth, frameHeight = initializeProgram()
    
    while (True):
        #Read frames
        ret, frame = capture.read()
        #new code
        if frame is None:
            break
        #Process video feed
        frame, firstFrame, text = processVideo(frame, args, firstFrame)
        #Display processed video feed
        displayVideo(frame, text)
        time.sleep(0.05)
        #Hotkey to break the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    closeProgram(capture)

#Script
if __name__ == "__main__":
    main()