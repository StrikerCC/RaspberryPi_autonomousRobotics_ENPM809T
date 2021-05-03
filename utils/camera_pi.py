# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 
import numpy as np
import sys, os

from imutils.video import VideoStream
import imutils
import time

sys.path.insert(0, os.path.dirname(os.getcwd()))


from RaspberryPi_autonomousRobotics_ENPM809T.utils.image import find_ROI
from RaspberryPi_autonomousRobotics_ENPM809T.utils.wheel import wheelControlled


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

    def angle_of_object(self, color_limit_object):
        frames_out = 10000

        print('looking for object like ', object, 'for', frames_out, 'frames')

        """find object in current frame"""
        for i in range(frames_out):
            img = self.view_one_frame()

            """find a contour around the object"""
            center, area = find_ROI(img, color_limit_object)
            radius = np.sqrt(area/2/np.pi)

            cv2.circle(img, center, int(radius), (255, 155, 155), 1)
            cv2.imshow(str(center), img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            """calculate the pixel coord"""
            angle = self.coord_img_to_pose(center)
            angle[0] = -(angle[0] + 2)

            if area > 5.0:    # if the pixel cluster is big enough
                """transform to img coord"""
                print('frame', i, 'found object at', angle, 'degree')
                return angle, img

            if i % 100 == 0:
                print('frame', i, 'haven\'t find object yet')

        return None, None


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
    wheel_ = wheelControlled()
    camera_ = camera_pi()
    color_ = {'low_limit': (91, 124, 88),
        'up_limit': (108, 255, 255)}
    angle, img = camera_.angle_of_object(color_)
    wheel_.rotate(angle)


if __name__ == '__main__':
    main()

