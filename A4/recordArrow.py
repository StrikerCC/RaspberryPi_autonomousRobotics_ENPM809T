# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 
from greenLightTracking import tracking

#from timeit import default_timer as timer 
import time 
from datetime import datetime


# initialize the Raspberry Pi camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 25
rawCapture = PiRGBArray(camera, size=(640,480))
# define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('greenLightTracking.avi', fourcc, 5, (640, 480))
tracker = tracking()

# open txt file to save data
f = open('hw3data.txt','a')

# allow the camera to warmup
time.sleep(0.1)

# keep looping
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=False):
    start = datetime.now()  # count time 

    # grab the current frame
    image = frame.array
    image = cv2.flip(image, 0)

    ### draw contour on the green light 
    image = tracker.showTracking(image)

    # show the frame to our screen
    cv2.imshow("Frame", image)
    
    # write frame to video file
    out.write(image)

    key = cv2.waitKey(10) & 0xFF
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    end = datetime.now() # count time 
    # print time to run through loop to the screen & save to file 
    dur = end-start 
    outstring = str(dur.total_seconds()) + '\n'
    f.write(outstring)
    print(outstring)

    # press the 'q' key to stop the video stream
    if key == ord("q"):
        # cv2.imwrite('green_light.jpg', image)
        break

out.release()
cv2.destroyAllWindows()


