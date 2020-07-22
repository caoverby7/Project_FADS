import cv2
import numpy as np


# Will accept video feed from first (zero-indexed) camera available to system (Usually a webcam)

cap = cv2.VideoCapture(0)

# initial location of window
r, h, c, w = 250, 200, 400, 150
track_window = (c, r, w, h)


# Background subtraction algorithm MOG

bgReduct = cv2.createBackgroundSubtractorMOG2()


# Save the resolution of the camera and print it to the console

frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(frameWidth, frameHeight)


# Continue loop as long as the video feed meets the resolution requirements

while (frameWidth >= 640 and frameHeight >= 480):

    # Returns true if the video feed still has frames left and then returns each frame from the video feed

    ret, frame = cap.read()

    # set up roi (region of interest) for tracking target
    roi = frame[r:r+h, c:c+w]
    # convert bgr to hsv(hue saturation value)
    hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # the range of color values to track
    mask = cv2.inRange(hsv_roi, np.array((100, 100, 100)),
                       np.array((255, 255, 255)))
    roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
    # normalizes the value range of an array
    cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
    # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
    term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

    # apply meanshift to get the new location
    ret, track_window = cv2.meanShift(dst, track_window, term_crit)

    # Draw it on display
    x, y, w, h = track_window
    img2 = cv2.rectangle(frame, (x, y), (x+w, y+h), 255, 2)

    # Convert each frame to grayscale

    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Create the foreground mask and apply it to the converted frame

    fgmask = bgReduct.apply(grayscale)

    # Display converted and masked feed

    cv2.imshow('vidFeed', fgmask)


# Wait for a 'Q' keypress, then break the loop
# A bitwise AND operation is used to return only the last byte (0xFF) from the key pressed
# The last byte will always be same for each key, but modifier keys can change bits further down
# Therefore by accepting only the last byte, any changes made by modifier keys will be ignored

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Important to release the capture after each time the program is finished running

cap.release()
cv2.destroyAllWindows()
