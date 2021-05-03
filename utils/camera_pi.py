# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 
import numpy as np

from imutils.video import VideoStream
import imutils
import time

class camera_pi():
    def __init__(self):
        # initialize the Raspberry Pi camera
        self.__camera = PiCamera()
        self.__resolution = (640, 480)
        self.__fov = (38.88, 38.88)               # full field of view in degree
        self.pixel_to_angle = float(self.__fov[0]) / float(self.__resolution[0])

        self.__camera.resolution = self.__resolution    # resolution
        self.__camera.framerate = 25                  # frame rate
        self.rawCapture = PiRGBArray(camera_pi, size=(640, 480))
        # define the codec and create VideoWriter object

        # allow the camera to warmup
        time.sleep(0.1)

    def view_one_frame(self):
        # grab the first frame
        for frame in self.__camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=False):
            image = frame.array
            image = cv2.flip(image, 0)
            # clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)
            return image

    def view_some_frames(self, num_frames=5, text=None):
        # keep looping for some frames
        i = 0
        for frame in self.__camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=False):
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
        for frame in self.__camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=False):
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
        for frame in self.__camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=False):
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

    def coord_img_to_pose(self, coord_img):
        """
        calculate the pose of a object according to it's image coordinates
        :param num_pixel: pixel coordinates of object of interesting
        :type num_pixel: tuple or np.array
        :return: object pose
        :rtype: numpy array
        """
        # angle = np.zeros((2,))
        """calculate the angle from center line to the pixel"""
        coord_img = coord_img - (np.array(self.__resolution) / 2)
        angle = coord_img * self.pixel_to_angle
        #assert 0.0 <= angle <= 360.0
        return angle

    def fov(self):
        return self.__fov

    def face_detect(self):
        # construct the argument parse and parse the arguments
        prototxt ='deploy.prototxt.txt',
        model = 'res10_300x300_ssd_iter_140000.caffemodel',
        confidence_min = 0.5,

        # load our serialized model from disk
        print("[INFO] loading model...")
        net = cv2.dnn.readNetFromCaffe(prototxt, model)

        print("[INFO] starting video stream...")
        vs = VideoStream(src=0).start()
        time.sleep(2.0)

        # loop over the frames from the video stream
        for i in range(100):
            # grab the frame from the threaded video stream and resize it
            # to have a maximum width of 400 pixels
            frame = vs.read()
            frame = imutils.resize(frame, width=400)

            # grab the frame dimensions and convert it to a blob
            (h, w) = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                         (300, 300), (104.0, 177.0, 123.0))

            # pass the blob through the network and obtain the detections and
            # predictions
            net.setInput(blob)
            detections = net.forward()

            # loop over the detections
            for i in range(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with the
                # prediction
                confidence = detections[0, 0, i, 2]

                # filter out weak detections by ensuring the `confidence` is
                # greater than the minimum confidence
                if confidence < confidence_min:
                    continue

                # compute the (x, y)-coordinates of the bounding box for the
                # object
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # draw the bounding box of the face along with the associated
                # probability
                text = "{:.2f}%".format(confidence * 100)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                              (0, 255, 0), 2)
                cv2.putText(frame, text, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
                # break
            # show the output frame
            cv2.imshow("Frame", cv2.flip(frame, -1))
            key = cv2.waitKey(1) & 0xFF

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break

        cv2.destroyAllWindows()


   
class recorder():
    def __init__(self, path):
        # initialize the Raspberry Pi camera
        self.camera = PiCamera()
        self.camera.__resolution = (640, 480)
        self.camera.framerate = 25
        self.rawCapture = PiRGBArray(camera_pi, size=(640, 480))

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

