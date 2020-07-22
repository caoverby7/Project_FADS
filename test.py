import cv2
import time
from datetime import datetime
import numpy as np
#import imutils

cap=cv2.VideoCapture(0)
logFile = open("Test_Event_Log.txt", "w+")
now = datetime.now()
logFile.write(now.strftime("%d/%m/%Y %H:%M:%S")+" --- "+"Program Initialized...\n"+now.strftime("%d/%m/%Y %H:%M:%S")+" --- "+"Log File Initialized...\n")
firstFrame = None
font = cv2.FONT_HERSHEY_SIMPLEX
while True:
    #Read and modify frames
    ret, frame = cap.read()
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gaussFrame = cv2.GaussianBlur(grayFrame, (9,9), 0)
    #Get the first frame
    if firstFrame is None:
        firstFrame = gaussFrame
        now = datetime.now()
        logFile.write(now.strftime("%d/%m/%Y %H:%M:%S")+" --- "+"First Frame Fetched\n")
        continue
    deltaFrame = cv2.absdiff(firstFrame, gaussFrame)
    threshFrame = cv2.threshold(deltaFrame, 25, 255, cv2.THRESH_BINARY)
    #Place timestamp on frame
    now = datetime.now()
    timeStamp = str(now.strftime("%d/%m/%Y %H:%M:%S"))
    frame = cv2.putText(frame, timeStamp, (5,400), font, 1, (0, 0, 255), 1)
    #Display frames in specific windows
    cv2.imshow("gray feed",grayFrame)
    cv2.imshow("Gaussian feed", gaussFrame)
    cv2.imshow("test feed", frame)
    cv2.imshow("delta", deltaFrame)
    #cv2.imshow("thresh", threshFrame)

    #Hotkey to break the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

logFile.close()
cap.release()
cv2.destroyAllWindows()