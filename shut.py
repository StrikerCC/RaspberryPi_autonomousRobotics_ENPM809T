# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 
from range01 import distance

# initialize the Raspberry Pi camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 25
rawCapture = PiRGBArray(camera, size=(640,480))
# define the codec and create VideoWriter object

# allow the camera to warmup
time.sleep(0.1)

# keep looping
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=False):
    # grab the current frame
    image = frame.array
    image = cv2.flip(image, 0)

    # show the frame to our screen
    cv2.imshow("Frame", image)
    
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # press the 'q' key to stop the video stream
    key = cv2.waitKey(10) & 0xFF
    if key == ord("q"):
        # dis = distance()
        # cv2.putText(image, "Distance: " + str(dis) + " cm", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        cv2.imwrite('greenArrowDown.jpg', image)
        break

cv2.destroyAllWindows()


