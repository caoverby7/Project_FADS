import cv2
import numpy as np
import matplotlib.pyplot as plt

# Will accept video feed from first (zero-indexed) camera available to system (Usually a webcam)
cap = cv2.VideoCapture(0)

frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(frameWidth, frameHeight)
print(cv2.CAP_PROP_FPS)

while (frameWidth >= 1280 and frameHeight >= 720):
    ret, frame = cap.read()

    # Convert each frame to grayscale
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('vidFeed', grayscale)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Important to release the capture after each time the program is finished running
cap.release()
cv2.destroyAllWindows()
