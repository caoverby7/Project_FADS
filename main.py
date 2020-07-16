import cv2
import numpy as np

# Will accept video feed from first (zero-indexed) camera available to system (Usually a webcam)
cap = cv2.VideoCapture(0)
# Background subtraction algorithm MOG
bgReduct = cv2.createBackgroundSubtractorMOG2()
# Save the resolution of the camera and print it to the console
frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(frameWidth, frameHeight)
# Continue loop as long as the video feed meets the resolution requirements
while (frameWidth >= 1280 and frameHeight >= 720):
    # Returns true if the video feed still has frames left and then returns each frame from the video feed
    ret, frame = cap.read()
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


#Loops
#detectMovement is a loop that contains compareFrames and checks to see if movement has occured if True, executes detectHumanoid
#def detectMovement():
#detectHumanoid is a lopp that contains compareFrames and checks if the source of movement is humoid, rather than a household pet. If True, executes followHumanoid
#def detectHumanoid()
#followHumanoid is a loop that follows the humanoid subject until it leaves view or fall is detected. If humanoid leaves, program executes resetProgram. If humanoid falls, program executes sendAlert
#def followHumanoid()

#Functions
#compareFrames takes the previous frame and current frame and compares them for the above loops
#def compareFrames()
    #We will want to pass the previous frame and current frame into this function. Recursion?
#sendAlert executes if subjectFallen = True. Afterwards, programs executes resetProgram
#def sendAlert()
    #Are we wanting to just make a pop-up message that says "fall detected?"
    #resetProgram()
#Resets all states to default to start in outer "main" loop
#def resetProgram()
    #movementDetected = False
    #subjectInFrame = False
    #subjectFallen = False

#States (Boolean)
#movementDetected = False
#subjectInFrame = False
#subjectFallen = False






# Important to release the capture after each time the program is finished running
cap.release()
cv2.destroyAllWindows()