# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 


class camera():
    def __init__(self):
        # initialize the Raspberry Pi camera
        self.camera = PiCamera()
        self.camera.__resolution = (640, 480)
        self.camera.framerate = 25
        self.rawCapture = PiRGBArray(camera, size=(640,480))
        # define the codec and create VideoWriter object

        # allow the camera to warmup
        time.sleep(0.1)

    def shut(self, path, text):
        
        # keep looping
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=False):
            # grab the current frame
            image = frame.array
            image = cv2.flip(image, 0)

            # show the frame to our screen
            cv2.imshow("Frame", image)
            
            # clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)

            # press the 'q' key to stop the video stream
            key = cv2.waitKey(10) & 0xFF
            if key == ord("q"):
                cv2.putText(image, text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                cv2.imwrite(path, image)
                break
        cv2.destroyAllWindows()

    def record(self, path, text):
        pass

def main():
    camera_ = camera()
    img_path = 'test.jpg'

    print('take a picture from pi camera, and store the image at ', img_path)

    camera_.shut(img_path, 'testing')

if __name__ == '__main__':
    main()

