# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 


class camera():
    def __init__(self):
        # initialize the Raspberry Pi camera
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 25
        self.rawCapture = PiRGBArray(camera, size=(640,480))
        # define the codec and create VideoWriter object

        # allow the camera to warmup
        time.sleep(0.1)

    def view_one_frame(self):
        # grab the first frame
        frame = self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=False)[0]
        image = frame.array
        image = cv2.flip(image, 0)
        # clear the stream in preparation for the next frame
        self.rawCapture.truncate(0)
        return image

    def view_some_frames(self, num_frames=5, text=None):
        # keep looping for some frames
        i = 0
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=False):
            i += 1
            # grab the current frame
            image = frame.array
            image = cv2.flip(image, 0)

            # write frame to video file
            if text:
                cv2.putText(image, text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            # show the frame to our screen
            cv2.imshow("Frame", image)

            # self.out.write(image)
            key = cv2.waitKey(1) & 0xFF
            # clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)

            # press the 'q' key to stop the video stream
            if i > num_frames or key == ord("q"):
                break

    def loop_until_shut(self, path, text):
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
                if text:
                    cv2.putText(image, text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                cv2.imwrite(path, image)
                break
        cv2.destroyAllWindows()

    def loop_and_record(self, path, text):
        # define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(path, fourcc, 5, (640, 480))

        # allow the camera to warmup
        time.sleep(0.5)

        # keep looping
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=False):
            # grab the current frame
            image = frame.array
            image = cv2.flip(image, 0)
            
            # write frame to video file
            #if text:
            cv2.putText(image, text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            # show the frame to our screen
            cv2.imshow("Frame", image)
            
            out.write(image)

            key = cv2.waitKey(10) & 0xFF
            # clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)

            # press the 'q' key to stop the video stream
            if key == ord("q"):
                break

        out.release()
        cv2.destroyAllWindows()

   
class recorder():
    def __init__(self, path):
        # initialize the Raspberry Pi camera
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 25
        self.rawCapture = PiRGBArray(camera, size=(640,480))

        # define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter(path, fourcc, 5, (640, 480))
        
        # allow the camera to warmup
        time.sleep(0.1)

    def __del__(self):
        self.out.release()
        cv2.destroyAllWindows()

    def record(self, num_frame, text=None):
        # allow the camera to warmup
        time.sleep(0.01)

        # keep looping for 10 frames
        i = 0
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=False):
            i += 1
            # grab the current frame
            image = frame.array
            image = cv2.flip(image, 0)
            
            # write frame to video file
            if text:
                cv2.putText(image, text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            # show the frame to our screen
            cv2.imshow("Frame", image)
            self.out.write(image)
            key = cv2.waitKey(1) & 0xFF
            # clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)

            # press the 'q' key to stop the video stream
            if i > num_frame or key == ord("q"):
                break

def main():
    record_ = recorder('test.avi')

    a = 'this is a testing video 0'
    record_.record(a)

    a = 'this is a testing video 1'
    record_.record(a)


if __name__ == '__main__':
    main()

