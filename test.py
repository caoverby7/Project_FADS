import cv2
import time
from datetime import datetime
import numpy as np

cap=cv2.VideoCapture(0)
logFile = open("Test_Event_Log.txt", "w+")
now = datetime.now()
logFile.write(now.strftime("%d/%m/%Y %H:%M:%S")+" --- "+"Program Initialized...\n"+now.strftime("%d/%m/%Y %H:%M:%S")+" --- "+"Log File Initialized...\n")
firstFrame = None
font = cv2.FONT_HERSHEY_SIMPLEX
while True:
    ret, frame = cap.read()
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gaussFrame = cv2.GaussianBlur(grayFrame, (9,9), 0)
    now = datetime.now()
    timeStamp = str(datetime.now())
    frame = cv2.putText(frame, timeStamp, (5,400), font, 1, (0, 0, 255), 1)
    cv2.imshow("gray feed",grayFrame)
    cv2.imshow("Gaussian feed", gaussFrame)
    cv2.imshow("test feed", frame)
    if firstFrame is None:
        firstFrame = gaussFrame
        now = datetime.now()
        logFile.write(now.strftime("%d/%m/%Y %H:%M:%S")+" --- "+"First Frame Fetched\n")
        continue
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

logFile.close()
cap.release()
cv2.destroyAllWindows()